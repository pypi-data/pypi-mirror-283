import numpy as np

from .CadenceDetectStateMachine import *
import music21 as m21
import math
import os
import pickle
import enum
import copy
import sys
import itertools

class CadenceDetector:
    def __init__(self,
                 maxNumMeasures=500,
                 minInitialMeasures=0,
                 minPostCadenceMeasures=0,
                 keyDetectionMode = CDKeyDetectionModes.KSWithSmoothingCadenceSensitive,
                 keyDetectionForgetFactor = 0.8,
                 reinforcementFactors=None,
                 keyDetectionLookahead = 0.5,
                 keyDetectionBlockSize=4,
                 keyDetectionOverlap=0.25,
                 completePickupFormat=False,
                 revertRebounds=True,
                 beatStrengthForGrouping=1.0,
                 includePicardy=False,
                 weightedKeyInterp=False):
        if reinforcementFactors is None:
            reinforcementFactors = {'PAC': 3, 'IAC': 1, 'HC': 3 / 2}
        self.MaxNumMeasures = maxNumMeasures
        self.KeyDetectionMode = keyDetectionMode
        self.KeyDetectionForgetFactor = keyDetectionForgetFactor
        self.ReinforcementFactors = reinforcementFactors
        self.key_detection_lookahead = keyDetectionLookahead
        self.blockSize = keyDetectionBlockSize
        self.overlap = keyDetectionOverlap
        self.HarmonicStateMachine = CDStateMachine(isChallenger=False, minInitialMeasures=minInitialMeasures, minPostCadenceMeasures=minPostCadenceMeasures, revertRebounds=revertRebounds, beatStrengthForGrouping=beatStrengthForGrouping, includePicardy=includePicardy)
        self.HarmonicStateMachineChallenger1 = CDStateMachine(isChallenger=True, minInitialMeasures=minInitialMeasures, minPostCadenceMeasures=minPostCadenceMeasures, revertRebounds=revertRebounds, beatStrengthForGrouping=beatStrengthForGrouping, includePicardy=includePicardy)
        self.HarmonicStateMachineChallenger2 = CDStateMachine(isChallenger=True, minInitialMeasures=minInitialMeasures, minPostCadenceMeasures=minPostCadenceMeasures, revertRebounds=revertRebounds, beatStrengthForGrouping=beatStrengthForGrouping, includePicardy=includePicardy)
        self.NoteStream = []
        self.NoteStream = []
        self.NoteStreamRestless = []
        self.NoteStreamReduced = []
        self.ChordStream = []
        self.ChordStreamRestless = []
        self.BassChords = []
        self.KeyPerMeasure = []
        self.CorrectedKeyPerMeasure = []
        self.InterpretationsPerMeasure = []
        self.InterpretationWeights = []
        self.SmoothedCorrCoefsPerMeasure = []
        self.CurrSmoothedInterpretations = {}
        #{'A': 0, 'B-': 0, 'B': 0, 'C': 0, 'C#': 0, 'D': 0,
        #'E-': 0, 'E': 0, 'F': 0, 'F#': 0, 'G': 0, 'A-': 0,
        #'a': 0, 'b-': 0, 'b': 0, 'c': 0, 'c#': 0, 'd': 0,
        #'e-': 0, 'e': 0, 'f': 0, 'f#': 0, 'g': 0, 'a-': 0}
        self.TopKeys = []
        self.PrevKeyString = []
        self.PrevChallenger1KeyString = []
        self.PrevChallenger2KeyString = []
        self.OptionalKeysPerMeasure = [[]]
        self.Parts = []
        self.MeasuresPerPart = []
        self.NumMeasures = 0
        self.fileName = 0
        self.hasPickupMeasure = 0
        self.completePickupFormat = completePickupFormat
        self.WritePath = 0
        self.RepeatedMeasureByVolta = []
        self.IncompleteMeasures = []
        self.EmptyMeasures = []
        self.FinalBarlines = []
        self.analysis_full = []
        self.analysis_filtered = []
        self.analysis_transition_strings = []
        self.PrevMeasureAlberti = False
        self.PrevMeasureArpeggio = False
        self.CadentialKeyChange = False
        self.AnchorRange = range(4,17)
        self.WeightedKeyInterp = weightedKeyInterp


    def loadMusic21Corpus(self,fileString):
        self.NoteStream = m21.corpus.parse(fileString)
        self.analyze()

    def loadFileAndGetMeasures(self, fileString):
        print("Loading score...")
        self.NoteStream = m21.converter.parse(fileString)
        self.Parts = self.NoteStream.recurse().getElementsByClass(m21.stream.Part)
        self.NumParts = len(self.Parts)
        for part in self.Parts:
            self.MeasuresPerPart.append(part.recurse().getElementsByClass(m21.stream.Measure))
        self.NumMeasures = max([len(curr_part_measures) for curr_part_measures in self.MeasuresPerPart])
        self.NumMeasures = min(self.NumMeasures, self.MaxNumMeasures)
        #update some data to state machines
        self.HarmonicStateMachine.NumParts = self.NumParts
        self.HarmonicStateMachineChallenger1.NumParts = self.NumParts
        self.HarmonicStateMachineChallenger2.NumParts = self.NumParts
        # do some other quick analysis for debugging without full cadence detection
        # self.findVoltas()

    def loadFile(self,fileString):
        self.loadFileAndGetMeasures(fileString)
        self.analyze()

    def analyze(self):
        self.removeChordSymbolsInNoteStream()
        self.removePickupMeasure()
        self.addMyLablesToParts(self.NoteStream)
        NoteStreamNoGrace = self.removeGraceNotes(self.NoteStream)
        try:
            self.ChordStream = NoteStreamNoGrace.chordify(addPartIdAsGroup=True, removeRedundantPitches=False, copyPitches=False)
            self.HarmonicStateMachine.CheckBassPartFromChord = True
            self.HarmonicStateMachineChallenger1.CheckBassPartFromChord = True
            self.HarmonicStateMachineChallenger2.CheckBassPartFromChord = True
        except:
            print("Cannot add parts to chords!!")
            self.ChordStream = NoteStreamNoGrace.chordify(removeRedundantPitches=False, copyPitches=False)
            self.HarmonicStateMachine.CheckBassPartFromChord = False
            self.HarmonicStateMachineChallenger1.CheckBassPartFromChord = False
            self.HarmonicStateMachineChallenger2.CheckBassPartFromChord = False


        self.NumMeasures = len(self.ChordStream.recurse().getElementsByClass(m21.stream.Measure))
        self.NumMeasures = min(self.NumMeasures, self.MaxNumMeasures)
        self.findVoltas()
        self.findFinalBarlines()
        self.findEmptyMeasures()
        self.findIncompleteMeasures()
        self.NoteStreamRestless = copy.deepcopy(self.NoteStream)  #create new list so as not to alter the original stream
        self.replaceBassRestsWithPrevsViaSecondsMaps()
        self.addMyLablesToParts(self.NoteStreamRestless)
        NoteStreamRestlessNoGrace = self.removeGraceNotes(self.NoteStreamRestless)
        if self.HarmonicStateMachine.CheckBassPartFromChord==True:
            self.ChordStreamRestless = NoteStreamRestlessNoGrace.chordify(addPartIdAsGroup=True, removeRedundantPitches=False, copyPitches=False)
        else:
            self.ChordStreamRestless = NoteStreamRestlessNoGrace.chordify(removeRedundantPitches=False, copyPitches=False)

        #chordifying only bass part
        parts = self.NoteStream.recurse().getElementsByClass(m21.stream.Part)
        BassPartNoGrace = self.removeGraceNotes(parts[-1])
        try:
            self.BassChords = BassPartNoGrace.chordify(addPartIdAsGroup=True, removeRedundantPitches=False, copyPitches=False)
        except:
            self.BassChords = BassPartNoGrace.chordify(removeRedundantPitches=False, copyPitches=False)

        self.findGroupLimitsViaSecondsMap()

    def findGroupLimitsViaSecondsMap(self):
        for part in self.Parts:
            prev_secondsDict = prev_note = prev_diff = []
            part_measures_secondsMap = sorted(part.recurse().getElementsByClass(m21.stream.Measure).secondsMap, key=lambda d: d['offsetSeconds'])
            part_notes_secondsMap = sorted(part.recurse().notesAndRests.secondsMap, key=lambda d: d['offsetSeconds'])
            for secondsDict in part_notes_secondsMap:
                curr_note = secondsDict['element']
                if curr_note.tie and not curr_note.tie == m21.tie.Tie('start'):
                    continue
                if prev_secondsDict:
                    curr_diff = secondsDict['offsetSeconds'] - prev_secondsDict['offsetSeconds']
                    if curr_diff <= 0:
                        continue
                    prev_note = prev_secondsDict['element']
                    if (prev_note.isRest and curr_note.isRest): # no grouping on consecutive rests
                        pass
                    elif not prev_note.isRest and curr_note.isRest:
                        prev_note.groups.append('}')
                    elif prev_note.isRest and not curr_note.isRest:
                        curr_note.groups.append('{')
                    elif prev_diff:
                        # long note groups backward with previous shorter notes
                        # also close grouping on very long notes (longer than a measure)
                        # epsilon and frac needed because they may be different due to fraction and measure duration inaccuracy
                        epsilon = 0.001
                        frac = 0.9
                        # === debug per measure
                        if curr_note.measureNumber and curr_note.measureNumber==66:
                            bla = 0
                        if (curr_diff > prev_diff + epsilon) or (prev_note.measureNumber and curr_diff >= frac * part_measures_secondsMap[prev_note.measureNumber-1]['durationSeconds']):
                            prev_note.groups.append('}')
                            curr_note.groups.append('{')
                    prev_diff = curr_diff
                else:  # first note of work
                    curr_note.groups.append('{')
                prev_secondsDict = secondsDict
            # always mark last note in part
            if prev_note:
                prev_note.groups.append('}')
            # add grouping lyrics for debug
            for note in part.recurse().getElementsByClass(m21.note.GeneralNote):
                note.lyric = ' '.join(note.groups)


    def findVoltas(self):
        self.RepeatedMeasureByVolta = [0] * self.NumMeasures
        RepeatBrackets = self.NoteStream.recurse().getElementsByClass('RepeatBracket')
        for repeat in RepeatBrackets:
            for sp_store in repeat.spannerStorage:
                measureIndex = sp_store.measureNumber - 1
                self.RepeatedMeasureByVolta[measureIndex] = 1

    def findFinalBarlines(self):
        self.FinalBarlines = [0] * self.NumMeasures
        final_barlines = self.NoteStream.recurse().getElementsByClass('Barline')
        for curr_barline in final_barlines:
            if curr_barline.type == 'final':
                measureIndex = curr_barline.measureNumber - 1
                self.FinalBarlines[measureIndex] = 1

    def measureContainsFinalBarline(self, measure):
        retVal = False
        barlines = measure.recurse().getElementsByClass('Barline')
        for curr_barline in barlines:
            if curr_barline.type == 'final':
                retVal = True
                break
        return retVal

    def measureContainsVolta(self, measure):
        retVal = False
        RepeatBrackets = measure.recurse().getElementsByClass('RepeatBracket')
        for repeat in RepeatBrackets:
            for _ in repeat.spannerStorage:
                retVal = True
                break
        return retVal

    def findIncompleteMeasures(self):
        print('Finding incomplete measures...')
        self.IncompleteMeasures = [0] * self.NumMeasures
        time_sig = []
        measure_zero = self.ChordStream.measure(0)
        if measure_zero:
            for currSig in measure_zero.recurse().getElementsByClass(m21.meter.TimeSignature):
                time_sig = currSig
        for i in range(self.NumMeasures): #enumerate(self.ChordStream.recurse().getElementsByClass(stream.Measure)):
            measure = self.ChordStream.measure(i+1)
            if measure:
                if i==36:
                    bla = 0
                for timeSig in measure.recurse().getElementsByClass(m21.meter.TimeSignature):
                    time_sig = timeSig
                chords = [chord for chord in measure.recurse().getElementsByClass('GeneralNote')]
                if chords and not chords[-1].isRest: # this attemps to avoid false pickups (i.e. ignore cases where the rest is just not long enough) - not sure this is solid for all pickups
                    lengths = [chord.duration.quarterLength for chord in chords]
                    total_duration = sum(lengths)
                    epsilon = 0.1 # this epsilon is needed because of inaccuracy caused by decoration notes in some scores
                    if total_duration < (1 - epsilon) * time_sig.barDuration.quarterLength:
                        self.IncompleteMeasures[i] = True
        # using pickup detection from Haydn, find first non-empty measure and set it incomplete there exists a pickup
        first_non_empty_measure = self.EmptyMeasures.index(0)
        self.IncompleteMeasures[first_non_empty_measure] = self.IncompleteMeasures[first_non_empty_measure] or self.hasPickupMeasure
        incomplete_measures = [i+1 for i,inc in enumerate(self.IncompleteMeasures) if inc]
        print('Incomplete meaures:', incomplete_measures)


    def findEmptyMeasures(self):
        print('Finding empty measures...')
        self.EmptyMeasures = [0] * self.NumMeasures
        for i in range(self.NumMeasures):
            curr_measure = self.ChordStream.measure(i+1)
            if curr_measure and len(curr_measure.recurse().notesAndRests) == 0:
                self.EmptyMeasures[i] = 1
        empty_measures = [i + 1 for i, emp in enumerate(self.EmptyMeasures) if emp]
        print('Empty measures:', empty_measures)

    def removePickupMeasure(self):
        if self.completePickupFormat:
            Parts = self.NoteStream.getElementsByClass(stream.Part)
            self.hasPickupMeasure = 1
            for part in Parts:
                if not part.flat.notesAndRests[0].isRest:
                    self.hasPickupMeasure = 0
                    print("Pickup Cancelled")
                    break

    def addMyLablesToParts(self, note_stream):
        parts = note_stream.recurse().getElementsByClass(m21.stream.Part)
        # for more than one voice, assuming soprano is first and bass last, remaining parts are not accessed individually
        parts[0].id = 'MySoprano'
        parts[-1].id = 'MyBasso'

    def removeGraceNotes(self, note_stream):
        # remove grace notes
        note_stream = copy.deepcopy(note_stream)
        graceNotes = []
        for n in note_stream.recurse().notes:
            if n.duration.isGrace:
                graceNotes.append(n)
        for grace in graceNotes:
            grace.activeSite.remove(grace)
        return note_stream

    def tryIsChord(x, self):
        try:
            return x.isChord
        except:
            return False

    def removeChordSymbolsInNoteStream(self):
        objects_to_remove = []
        for curr_note in self.NoteStream.recurse().getElementsByClass('ChordSymbol'):
            if curr_note.isChord:
                objects_to_remove.append(curr_note)

        self.NoteStream.remove(objects_to_remove,recurse=True)

        chords_present = False
        for curr_note in self.NoteStream.recurse().getElementsByClass(note.GeneralNote):
            if curr_note.isChord:
                chords_present = True
                break
        if not chords_present:
             print('No more chords in note stream!')

    def replaceBassRestsWithPrevsViaSecondsMaps(self):
        max_consec_empty_meas = 1
        prev_note = []
        prev_measure_dur = []
        consecutive_empty_measure_durations = []
        measures_to_tie = []
        parts = self.NoteStreamRestless.recurse().getElementsByClass(m21.stream.Part)
        for curr_measure in parts[-1].recurse().getElementsByClass(m21.stream.Measure):
            notes_in_measure = 0
            measure_modifcations_list = []
            if curr_measure.measureNumber == 121:
                bla  = 0
            # get curr meaure duration before alterations
            curr_measure_duration = copy.deepcopy(curr_measure.duration.quarterLength)
            #find rest and create modifications
            sortedSecondsMaps = sorted(curr_measure.recurse().secondsMap, key=lambda d: d['offsetSeconds'])
            for curr_item in sortedSecondsMaps:
                #only notes, chords, and rests have durations
                if not curr_item['durationSeconds'] > 0:
                    continue
                if curr_item['element'].isRest:# found rest, remove it but not after one measure
                    if prev_note and (notes_in_measure > 0 or len(consecutive_empty_measure_durations) <= max_consec_empty_meas):
                        measure_modifcations_list.append(curr_item['element'])
                else: # note or chord
                    if not prev_note:
                        prev_note = curr_item
                    else: # not a rest and prev_note exists
                        if notes_in_measure > 0 and (curr_item['element'].offset == prev_note['element'].offset or curr_item['endTimeSeconds'] == prev_note['endTimeSeconds']):# if has same offset but lower bass update new curr item without changing duration
                            curr_lowest_pitch = curr_item['element'].sortFrequencyAscending().pitches[0] if curr_item['element'].isChord else curr_item['element'].pitch
                            prev_lowest_pitch = prev_note['element'].sortFrequencyAscending().pitches[0] if prev_note['element'].isChord else prev_note['element'].pitch
                            if curr_lowest_pitch.midi < prev_lowest_pitch.midi:
                                prev_note = curr_item
                        else: # found note or chord with new offset, extend duration till this note
                            curr_offset = curr_item['element'].offset
                            prev_offset = prev_note['element'].offset
                            extended_quarterLength = curr_offset - prev_offset
                            if notes_in_measure == 0 and prev_measure_dur: # first note in measure, complete previous measure
                                extended_quarterLength += prev_measure_dur
                            # now complete the empty measues (if exist)
                            extended_quarterLength += np.sum([dur for dur in consecutive_empty_measure_durations])
                            if extended_quarterLength > prev_note['element'].quarterLength and (notes_in_measure > 0 or len(consecutive_empty_measure_durations) <= max_consec_empty_meas):
                                prev_note['element'].duration = m21.duration.Duration(extended_quarterLength)
                                prev_note['element'].quarterLength = extended_quarterLength
                            # now check if prev_note exceeded its measure length
                            if (prev_note['element'].offset + prev_note['element'].quarterLength > curr_measure_duration):
                                measures_to_tie.append({'from': prev_note['element'].measureNumber, 'to': curr_measure.measureNumber})
                            prev_note = curr_item
                    notes_in_measure += 1
                    consecutive_empty_measure_durations = []
            #extend last note to complete measure
            if prev_note and notes_in_measure > 0:
                remainder = curr_measure_duration - prev_note['element'].offset
                if remainder > prev_note['element'].quarterLength:
                    prev_note['element'].duration = m21.duration.Duration(remainder)
                    prev_note['element'].quarterLength = remainder
            # check for final barline
            if curr_measure.rightBarline and curr_measure.rightBarline.type == 'final':
                prev_note = []
            # check if measure was empty
            if notes_in_measure == 0 and prev_note:
                consecutive_empty_measure_durations.append(curr_measure.duration.quarterLength)
            prev_measure_dur = curr_measure.duration.quarterLength
            # make erase modifications to measure
            curr_measure.remove(measure_modifcations_list, recurse=True)
        # making ties for notes extending beyond measure locally
        makeTies_local_failure = False
        for curr_measures_to_tie in measures_to_tie:
            try:
                self.NoteStreamRestless.parts[-1].measures(curr_measures_to_tie['from'], curr_measures_to_tie['to']).recurse().makeTies(inPlace=True)
            except:
                makeTies_local_failure = True
                print(f'makeTies failed on measures {curr_measures_to_tie}')
        # making ties on entire stream if it failed locally
        if makeTies_local_failure:
            try:
                self.NoteStreamRestless.parts[-1].recurse().makeTies(inPlace=True)
                print(f'makeTies overall succeeded')
            except:
                print(f'makeTies failed')
        else:
            print(f'makeTies locally succeeded')

    def noteFromRestWithPitch(self,rest,pitch):
        noteFromRest = m21.note.Note(pitch)
        noteFromRest.duration = rest.duration
        noteFromRest.offset = rest.offset
        noteFromRest.quarterLength = rest.quarterLength
        return noteFromRest

    def chordFromRest(self,rest):
        chordFromRest = m21.chord.Chord([])
        chordFromRest.duration = rest.duration
        chordFromRest.offset = rest.offset
        chordFromRest.quarterLength = rest.quarterLength
        return chordFromRest


    def getNumMeasures(self):
        return self.NumMeasures

    def detectKeyPerMeasure(self):
        print("Detecting key per block...")
        print("Num Measures:", self.NumMeasures)
        for currBlock in range(1, self.NumMeasures+1):
            # this only looks at current bar and backwards, simulating realtime
            lookahead = round((self.blockSize - 1) * self.key_detection_lookahead)
            lookback = self.blockSize - lookahead - 1
            StopMeasure = min(currBlock + lookahead, self.NumMeasures)
            StartMeasure = max(currBlock - lookback, 0)
            CurrMeasures = self.NoteStream.measures(StartMeasure, StopMeasure)
            #print(currBlock, StopMeasure)
            try:
                #analysisClasses = [
                #    Ambitus,
                #    KrumhanslSchmuckler,
                #    AardenEssen,
                #    SimpleWeights,
                #    BellmanBudge,
                #    TemperleyKostkaPayne,
                #]
                Key = CurrMeasures.analyze('TemperleyKostkaPayne')
                Key.alternateInterpretations.append(Key)
                CurrInterpretations = list(Key.alternateInterpretations)
            except:
                print("Key detection error:", sys.exc_info()[0])
                print("Maintaining previous key")
                CurrInterpretations = list(self.InterpretationsPerMeasure[-1])

            self.InterpretationsPerMeasure.append(CurrInterpretations)
            # weight by number of notes per block
            self.InterpretationWeights.append(len(CurrMeasures.recurse().notes))
        # normalize weights
        self.InterpretationWeights = self.InterpretationWeights/np.max(self.InterpretationWeights)

    def setConstantKeyPerMeasure(self, key_string):
        const_key = m21.key.Key(key_string)
        const_key.correlationCoefficient = 1.0
        dummy_key_string = 'C' if key_string != 'C' else 'A'
        dummy_key = m21.key.Key(dummy_key_string)
        dummy_key.correlationCoefficient = 0.0
        const_key_list = [const_key, dummy_key]
        for m in range(1, self.NumMeasures + 1):
            self.InterpretationsPerMeasure.append(const_key_list)

    def reenforceKeyByFactor(self, keyString, enhancement):
        enhancedCoef = math.pow(self.CurrSmoothedInterpretations[keyString], 1/enhancement)
        self.CurrSmoothedInterpretations[keyString] = enhancedCoef

    def writeKeyPerMeasureToFile(self):
        if self.KeyDetectionMode != CDKeyDetectionModes.KSWithSmoothingCadenceSensitive:
            print("Writing keys to file...")
            keyfileName = self.fileName.replace(".", "_")
            FullPath = os.path.join(self.WritePath, keyfileName)
            KeyFile = f"{FullPath}_Key_{self.KeyDetectionMode}.txt"
            with open(KeyFile, 'wb') as f:
                pickle.dump(self.KeyPerMeasure, f)

    def readKeyPerMeasureFromFile(self):
        if self.KeyDetectionMode != CDKeyDetectionModes.KSWithSmoothingCadenceSensitive:
            print("Reading keys from file...")
            keyfileName = self.fileName.replace(".", "_")
            FullPath = os.path.join(self.WritePath, keyfileName)
            KeyFile = f"{FullPath}_Key_{self.KeyDetectionMode}.txt"
            with open(KeyFile, 'rb') as f:
                self.KeyPerMeasure=pickle.load(f)

    def getKeyPerMeasureFromSearsFile(self,FullPath):
        FullPath = FullPath.replace(".xml", ".txt")

        class SearKeyDataIndices(enum.IntEnum):
            Key = 0
            Mode = 1
            StartBar = 2
            StartPulse = 3
            EndBar = 4
            EndPulse = 5

        with open(FullPath,'r') as f:
            lines = f.readlines()
            FoundRow = 0
            totalNumMeasures = 0
            startMeasure = 0
            endMeasure = -1
            for line in lines:
                if FoundRow==0:
                    if "Tonal Region" in line:
                        FoundRow = 1
                        continue
                else:
                    if "Major" in line or "Minor" in line:
                        elements = line.strip().split("\t")
                        currKey = self.mapSearsKeyToMusic21Key(elements[SearKeyDataIndices.Key],elements[SearKeyDataIndices.Mode])
                        print(elements, len(elements))
                        #print(line, file=text_file_reduced)
                        startMeasure = elements[SearKeyDataIndices.StartBar]

                        if "Begin" in startMeasure:
                            startMeasure = 1
                        else:
                            startMeasure = int(startMeasure)

                        # check if start measure is before prev end measure then there is an overlap in tonal regions (TBD - what to do with this?)
                        if startMeasure<=endMeasure:
                            startMeasure = endMeasure + 1

                        endMeasure = elements[SearKeyDataIndices.EndBar]
                        if "End" in endMeasure:
                            endMeasure = self.NumMeasures
                        else:
                            endMeasure = int(endMeasure)

                        numMeasuresToAppend = endMeasure-startMeasure+1 #including start and end

                        for i in range(numMeasuresToAppend):
                            self.KeyPerMeasure.append(currKey)

            print("KeysLen=", len(self.KeyPerMeasure))
            print("NumMeasures=",self.NumMeasures)

    def mapSearsKeyToMusic21Key(self,SearStringKey, SearStringMode):
        Music21StringKey = SearStringKey.replace("b","-")
        Music21StringMode = SearStringMode.replace("M","m")
        return m21.key.Key(Music21StringKey,Music21StringMode)

    def isArpeggioPattern(self, pitches, lengths, arp_len, up_down=None):
        if len(pitches) < arp_len or not all(lengths[0] == l for l in lengths[1:-1]): # the final note in an arpeggio can be longer
            retVal = False
        else:
            intervals = np.diff([x.midi for x in pitches])
            if up_down == 'up':
                monotonic_rising = np.all(intervals > 0)
                num_seconds = np.count_nonzero(intervals < 3)
                retVal = monotonic_rising and num_seconds <= 1 # allow one major or minor second
            elif up_down == 'down':
                monotonic_falling = np.all(intervals < 0)
                num_seconds = np.count_nonzero(intervals > -3)
                retVal = monotonic_falling and num_seconds <= 1 # allow one major or minor second
            else:
                retVal = False
        return retVal

    def isAlbertiPattern(self, pitches, lengths, pattern_len):
        equal_durations = all(lengths[0] == l for l in lengths[1:4])
        lowest_pitch_first = all(x.midi >= pitches[0].midi for x in pitches[1:4])
        lowest_pitch_third = all(x.midi >= pitches[2].midi for x in pitches[1:4])
        repetitve_pitch = (pitches[1].midi == pitches[3].midi or pitches[0].midi == pitches[2].midi)
        consecutive_pitch = (lowest_pitch_first and pitches[0].midi == pitches[1].midi) or (lowest_pitch_third and pitches[2].midi == pitches[1].midi)
        # for pattern length 6 (3/4,3/8,6/8) verify last two as well, either continuing the same pattern or repeating the bass
        if pattern_len == 6:
            equal_durations = all(lengths[0] == l for l in lengths)
            repetitve_pitch = repetitve_pitch and (pitches[3].midi == pitches[5].midi or pitches[0] == pitches[4])
        is_alberti = equal_durations and repetitve_pitch and (lowest_pitch_first or lowest_pitch_third) and not consecutive_pitch
        bass_pitch_index = None
        if lowest_pitch_first:
            bass_pitch_index = 0
        elif lowest_pitch_third:
            bass_pitch_index = 2
        return is_alberti, bass_pitch_index

    def extractBassLine(self, measure):
        lowestPitches = []
        quarterLengths= []
        for chord in measure:
            if not chord.isRest:
                lowestNote = chord.sortFrequencyAscending()[0]
                lowestPitches.append(lowestNote.pitch)
                quarterLengths.append(lowestNote.quarterLength)
            else:
                lowestPitches.append(None)
        return {'pitches': lowestPitches, 'lengths': quarterLengths}

    def detectAlbertiOrArpeggioBassInMeasure(self, measure_chords, bass_chords, pattern_len, arp_type):
        #first exact bassline from chords
        measure_general_notes = measure_chords.recurse().getElementsByClass('GeneralNote')
        bass_general_notes = bass_chords.recurse().getElementsByClass('GeneralNote')
        lowest_pitches_in_bass = self.extractBassLine(bass_general_notes)
        arp_patterns = []

        # need to loop like this because we advance the index based on finding arpeggios
        i = 0
        while i <= len(bass_general_notes)-pattern_len:
            curr_pitches = lowest_pitches_in_bass['pitches'][i:i+pattern_len]
            curr_lengths = lowest_pitches_in_bass['lengths'][i:i+pattern_len]
            isArp = False
            if None not in curr_pitches:
                if any([cl > 1 for cl in curr_lengths]): # do not consider arps greater than quarter notes
                    isArp = False
                elif arp_type == 'alberti':
                    isArp, bass_pitch_index = self.isAlbertiPattern(pitches=curr_pitches, lengths=curr_lengths, pattern_len=pattern_len)
                elif arp_type == 'arp_up':
                    isArp = self.isArpeggioPattern(pitches=curr_pitches, lengths=curr_lengths, arp_len=pattern_len, up_down='up')
                    bass_pitch_index = 0
                elif arp_type =='arp_down':
                    isArp = self.isArpeggioPattern(pitches=curr_pitches, lengths=curr_lengths, arp_len=pattern_len, up_down='down')
                    bass_pitch_index = 0
                else:
                    isArp = False
                if isArp:
                    epsilon = 0.1  # this epsilon is required to mark the last alberti beat including its length, but not the next beat
                    # already assuming they are all equal length
                    beat_diff = bass_general_notes[i+1].beat-bass_general_notes[i].beat # for some reason quarter length does not always provide this, TBD use seconds map
                    if bass_pitch_index == 0:
                        arp_patterns.append({'start': bass_general_notes[i + 1].beat,
                                             'stop': bass_general_notes[i + pattern_len - 1].beat + beat_diff - epsilon})
                    else:
                        # mark from beginning of pattern not including first note, to bass pitch index not included
                        arp_patterns.append({'start': bass_general_notes[i + 1].beat,
                                             'stop': bass_general_notes[i + bass_pitch_index - 1].beat + beat_diff - epsilon})
                        # mark from note after bass pitch index to the end
                        arp_patterns.append({'start': bass_general_notes[i + bass_pitch_index + 1].beat,
                                             'stop': bass_general_notes[i + pattern_len - 1].beat + beat_diff - epsilon})
            # advance index by pattern length if alberti found, otherwise advance to next beat
            i = i + pattern_len if isArp else i + 1


        arp_beats = [0] * len(measure_general_notes)
        for i,gen_note in enumerate(measure_general_notes):
            for pat in arp_patterns:
                if pat['start'] <= gen_note.beat <= pat['stop']:
                    arp_beats[i] = True
                    break

        return arp_beats

    def smoothKeyInterpretations(self, measureIndex):
        currInterpretations = self.InterpretationsPerMeasure[measureIndex]
        if self.WeightedKeyInterp:
            currWeight = self.InterpretationWeights[measureIndex]
            currForgetFactor = 0.5 * (self.KeyDetectionForgetFactor + (1-currWeight))
        else:
            currForgetFactor = self.KeyDetectionForgetFactor
        for interpretation in currInterpretations:
            corrCoef = interpretation.correlationCoefficient
            keyString = interpretation.tonicPitchNameWithCase
            if keyString not in self.CurrSmoothedInterpretations:
                self.CurrSmoothedInterpretations[keyString] = corrCoef
            currSmoothedVal = self.CurrSmoothedInterpretations[keyString]
            currSmoothedVal = currForgetFactor * currSmoothedVal + (1-currForgetFactor) * corrCoef
            self.CurrSmoothedInterpretations[keyString] = currSmoothedVal

    def resetSmoothedInterpretations(self):
        self.CurrSmoothedInterpretations = {}

    def getTopNKeyInterpretations(self, N):
        #now sort by value
        SortedKeys = sorted(self.CurrSmoothedInterpretations.items(), key=lambda x: x[1], reverse=True)
        TopNKeys = list(SortedKeys[:N])
        return TopNKeys


    def getNotesPerChordBeatPerPart(self, ChordsMeasure, NotesMeasure):
        Parts = NotesMeasure.recurse().getElementsByClass(m21.stream.Part)
        parts_flat = [part.flat.notesAndRests for part in Parts]
        notesPerChordBeatPerPart = [[[real_note for real_note in part if chord.beat == real_note.beat] for part in parts_flat] for chord in ChordsMeasure.recurse().getElementsByClass('GeneralNote')]
        return notesPerChordBeatPerPart


    def detectCadences(self):
        print("Detecting cadences...")
        self.analysis_full = []
        self.analysis_transition_strings = []

        measuresSecondsMap = list(filter(lambda d: d['durationSeconds'] > 0, self.ChordStreamRestless.secondsMap))

        prevState = []
        repeat_counter = 0
        incomplete_counter = 0
        empty_measure_counter = 0
        coefs_per_measure = []

        # check first timesig
        measure_zero = self.ChordStream.measure(0)
        curr_time_sig = self.check_and_update_timesig(measure_zero, [])

        # loop on measures:
        try:
            # === for debugging a measure range
            # range_with_holes = itertools.chain(range(0, 4), range(10, 20))
            # for currMeasureIndex in range_with_holes:
            for currMeasureIndex in range(0,self.NumMeasures):
                # debug per measure
                if currMeasureIndex == 7:
                    bla = 0
                # true measures start with 1, pickups will start from zero, but not all corpora will abide to this
                # for example, data that originates from midi cannot contain this info
                # to overcome this, we attempt to find the pickup via initial rests and discard it
                # also, we count the empty measures and index them out while writing the label
                measure_number = currMeasureIndex + 1
                # print(f"measure number {measure_number}")
                CurrMeasuresRestless = self.ChordStreamRestless.measure(measure_number)
                CurrMeasures = self.ChordStream.measure(measure_number)
                CurrMeasuresNotes = self.NoteStream.measure(measure_number)
                CurrMeasureBass = self.BassChords.measure(measure_number)

                # state machines need this for their first counters
                isPickupMeasure = measure_number == 1 and self.hasPickupMeasure
                self.HarmonicStateMachine.IsPickupMeasure = isPickupMeasure
                self.HarmonicStateMachineChallenger1.IsPickupMeasure = isPickupMeasure
                self.HarmonicStateMachineChallenger2.IsPickupMeasure = isPickupMeasure

                # check and update timesig
                curr_time_sig = self.check_and_update_timesig(CurrMeasures, curr_time_sig)

                # reset state machines after repeat brackets, unless cadence inevitable (TBD  - add double barlines to this)
                if currMeasureIndex > 0 and self.FinalBarlines[currMeasureIndex-1] and not (self.HarmonicStateMachine.getCadentialOutput() == CDCadentialStates.CadInevitable):
                    self.HarmonicStateMachine.reset()
                    self.HarmonicStateMachineChallenger1.reset()
                    self.HarmonicStateMachineChallenger2.reset()
                    self.resetSmoothedInterpretations()

                if self.EmptyMeasures[currMeasureIndex]:
                    empty_measure_counter = empty_measure_counter + 1
                    continue

                if self.IncompleteMeasures[currMeasureIndex]:
                    incomplete_counter = incomplete_counter + 1

                if not CurrMeasures or not CurrMeasuresRestless:
                    continue

                NotesPerChordBeatPerPart = self.getNotesPerChordBeatPerPart(CurrMeasures, CurrMeasuresNotes)

                AlbertiBeats4 = self.detectAlbertiOrArpeggioBassInMeasure(CurrMeasuresRestless, CurrMeasureBass, pattern_len=4, arp_type='alberti')
                AlbertiBeats = AlbertiBeats4
                if curr_time_sig.ratioString in ['3/4', '6/8', '3/8']:
                    AlbertiBeats6 = self.detectAlbertiOrArpeggioBassInMeasure(CurrMeasuresRestless, CurrMeasureBass, pattern_len=6, arp_type='alberti')
                    AlbertiBeats = [x or y for (x, y) in zip(AlbertiBeats4, AlbertiBeats6)]

                # consider Alberti only after the second consecutive measure
                # AlbertiBeatsFiltered = [x and self.PrevMeasureAlberti for x in AlbertiBeats]
                # self.PrevMeasureAlberti = any(AlbertiBeats)

                ArpeggioBeats4 = self.detectAlbertiOrArpeggioBassInMeasure(CurrMeasuresRestless, CurrMeasureBass, pattern_len=4, arp_type='arp_up')
                ArpeggioBeats = ArpeggioBeats4
                if curr_time_sig.ratioString in ['3/4', '6/8', '3/8']:
                    ArpeggioBeats3 = self.detectAlbertiOrArpeggioBassInMeasure(CurrMeasuresRestless, CurrMeasureBass, pattern_len=3, arp_type='arp_up')
                    ArpeggioBeats = [x or y for (x, y) in zip(ArpeggioBeats3, ArpeggioBeats4)]

                # consider Arpeggio only after the second consecutive measure
                ArpeggioBeatsFiltered = [x and self.PrevMeasureArpeggio for x in ArpeggioBeats]
                self.PrevMeasureArpeggio = any(ArpeggioBeats)

                LyricPerBeat = []

                if self.KeyDetectionMode == CDKeyDetectionModes.KSWithSmoothing or\
                        self.KeyDetectionMode==CDKeyDetectionModes.KSWithSmoothingCadenceSensitive:
                    #smooth keys here, per measure (TBD - per chord?):
                    self.smoothKeyInterpretations(currMeasureIndex)
                    #sort and return top 2
                    self.TopKeys = self.getTopNKeyInterpretations(3)
                else:
                    currKey = self.KeyPerMeasure[currMeasureIndex]#lists start with 0

                for thisChord, thisChordWithBassRests, alberti, arpeggio, thisRealNotes in zip(CurrMeasuresRestless.recurse().getElementsByClass('GeneralNote'),CurrMeasures.recurse().getElementsByClass('GeneralNote'), AlbertiBeats, ArpeggioBeatsFiltered, NotesPerChordBeatPerPart):
                    if self.KeyDetectionMode == CDKeyDetectionModes.KSWithSmoothing or\
                            self.KeyDetectionMode == CDKeyDetectionModes.KSWithSmoothingCadenceSensitive:
                        currKeyString = self.TopKeys[0][0]
                        currKey = m21.key.Key(currKeyString)
                        challenger1KeyString = self.TopKeys[1][0]
                        challenger1Key = m21.key.Key(challenger1KeyString)
                        challenger2KeyString = self.TopKeys[2][0]
                        challenger2Key = m21.key.Key(challenger2KeyString)
                        self.updateKeysAndSwapStateMachines(currKeyString, challenger1KeyString, challenger2KeyString)

                    # main key state machine
                    if thisChordWithBassRests.isRest:
                        self.HarmonicStateMachine.updateHarmonicState(currKey, thisChord, thisChordWithBassRests, [], [], [], alberti, arpeggio, [], thisRealNotes)
                    else:
                        rn = m21.roman.romanNumeralFromChord(thisChordWithBassRests, currKey)
                        self.HarmonicStateMachine.updateHarmonicState(currKey, thisChord, thisChordWithBassRests, rn.scaleDegree, rn.inversion(), rn.figure, alberti, arpeggio, rn, thisRealNotes)

                    # challenger key state machine
                    if self.KeyDetectionMode == CDKeyDetectionModes.KSWithSmoothing or self.KeyDetectionMode == CDKeyDetectionModes.KSWithSmoothingCadenceSensitive:
                        if thisChordWithBassRests.isRest:
                            self.HarmonicStateMachineChallenger1.updateHarmonicState(challenger1Key, thisChord, thisChordWithBassRests, [], [], [], alberti, arpeggio, [], thisRealNotes)
                            self.HarmonicStateMachineChallenger2.updateHarmonicState(challenger2Key, thisChord, thisChordWithBassRests, [], [], [], alberti, arpeggio, [], thisRealNotes)
                        else:
                            rn2 = m21.roman.romanNumeralFromChord(thisChordWithBassRests, challenger1Key)
                            self.HarmonicStateMachineChallenger1.updateHarmonicState(challenger1Key, thisChord, thisChordWithBassRests, rn2.scaleDegree, rn2.inversion(), rn2.figure, alberti, arpeggio, rn2, thisRealNotes)
                            rn2 = m21.roman.romanNumeralFromChord(thisChordWithBassRests, challenger2Key)
                            self.HarmonicStateMachineChallenger2.updateHarmonicState(challenger2Key, thisChord, thisChordWithBassRests, rn2.scaleDegree, rn2.inversion(), rn2.figure, alberti, arpeggio, rn2, thisRealNotes)

                    #TBD - should we handle this reversion in challenger?
                    if self.HarmonicStateMachine.getRevertLastPACAndReset() and len(LyricPerBeat) > 0: #this limits PAC reversion to within measure
                        LastPACTuple = LyricPerBeat[-1]
                        UpdatedLyric = "IAC"
                        LyricPerBeat[-1] = [LastPACTuple[0], UpdatedLyric]
                        print("Reverting last PAC to IAC")
                    if self.HarmonicStateMachine.getRevertLastHCAndReset() and len(LyricPerBeat) > 0:  # this limits HC reversion to within measure
                        LastHCTuple = LyricPerBeat[-1]
                        UpdatedLyric = ""
                        LyricPerBeat[-1] = [LastHCTuple[0], UpdatedLyric]
                        print("Reverting last HC")
                    if self.HarmonicStateMachine.getRevertLastIACAndReset() and len(LyricPerBeat) > 0:  # this limits IAC reversion to within measure
                        LastIACTuple = LyricPerBeat[-1]
                        UpdatedLyric = ""
                        LyricPerBeat[-1] = [LastIACTuple[0], UpdatedLyric]
                        print("Reverting last IAC")

                    Lyric = self.HarmonicStateMachine.getCadentialOutputString()
                    LyricChallenger1 = self.HarmonicStateMachineChallenger1.getCadentialOutputString()
                    LyricChallenger2 = self.HarmonicStateMachineChallenger2.getCadentialOutputString()
                    # Cadence Sensitive Key Detection Mode
                    if self.KeyDetectionMode == CDKeyDetectionModes.KSWithSmoothingCadenceSensitive:
                        # and self.HarmonicStateMachineChallenger.CurrHarmonicState.Key.tonic != self.HarmonicStateMachine.CurrHarmonicState.Key.tonic: #don't be sensitive to candece in parallel key:
                        # Cadence check in main key (for key re-enforcement)

                        resort = False
                        self.CadentialKeyChange = False
                        for cad in self.ReinforcementFactors:
                            if cad in Lyric:
                                # avoid reinforcement of HC if challenger is on dominant
                                reenforce = not (currKey.getDominant().pitchClass == challenger1Key.tonic.pitchClass and challenger1Key.mode=='major' and (cad == 'HC'))
                                if reenforce:
                                    self.reenforceKeyByFactor(currKeyString, self.ReinforcementFactors[cad])
                            # Challenger Check (for key switching, but ignore HCs in subdominant key (becuase they are more likely PACs in main key))
                            if cad in LyricChallenger1:
                                reenforce =  not (challenger1Key.tonic.pitchClass == self.getSubDominantPitchClass(currKey) and challenger1Key.mode=='major' and (cad == 'HC'))
                                if reenforce:
                                    self.reenforceKeyByFactor(challenger1KeyString, self.ReinforcementFactors[cad])
                                    resort = True
                            if cad in LyricChallenger2:
                                reenforce =  not (challenger2Key.tonic.pitchClass == self.getSubDominantPitchClass(currKey) and challenger2Key.mode=='major' and (cad == 'HC'))
                                if reenforce:
                                    self.reenforceKeyByFactor(challenger2KeyString, self.ReinforcementFactors[cad])
                                    resort = True
                        if resort:
                            # re-sort and return Top2Keys
                            self.TopKeys = self.getTopNKeyInterpretations(3)
                            if challenger1KeyString == self.TopKeys[0][0]:
                                Lyric = LyricChallenger1
                                self.CadentialKeyChange = True
                                print('Cadential Key Change!')
                            if challenger2KeyString == self.TopKeys[0][0]:
                                Lyric = LyricChallenger2
                                self.CadentialKeyChange = True
                                print('Cadential Key Change!')


                    # debugging
                    # print(self.HarmonicStateMachine.getCadentialOutput().value)
                    # thisChord.lyric = str(rn.figure)
                    # for debugging albertis and arppeggios
                    # if alberti or arpeggio:
                    #    Lyric = Lyric + 'Al'

                    if Lyric:   # only work on non-empty lyrics
                        thisChord.lyric = Lyric
                        # switching between major and minor of same key (parallel keys), keep the PAC
                        #if challengerKey.tonic.pitchClass == currKey.tonic.pitchClass and 'PAC' in LyricChallenger:
                        #    thisChord.lyric = Lyric + LyricChallenger
                        LyricPerBeat.append([thisChord.beat,thisChord.lyric])
                        #TBD - do we still need to print this?
                        self.analysis_transition_strings.append(f"{measuresSecondsMap[currMeasureIndex]['offsetSeconds'] + measuresSecondsMap[currMeasureIndex]['durationSeconds']*(thisChord.beat-1)/CurrMeasuresRestless.duration.quarterLength:.1f} {self.HarmonicStateMachine.getCadentialOutput().value}")

                #checking cadences on entire measure
                for LyricTuple in LyricPerBeat:
                    Lyric = LyricTuple[1]
                    LyricsToPrint = ["PAC", "IAC", "HC", "PCC", "PCH"]
                    if any([s in Lyric for s in LyricsToPrint]):
                        # incomplete and empty counters count measures that should be discarded
                        measure_to_write = measure_number - self.hasPickupMeasure - empty_measure_counter
                        print('Measure ', measure_to_write, ' offset ', measuresSecondsMap[currMeasureIndex]['offsetSeconds'], " ", Lyric)
                        self.analysis_full.append({"Measure": measure_to_write, "Offset": measuresSecondsMap[currMeasureIndex]['offsetSeconds'], "Lyric": Lyric})
                    elif "Key" in Lyric:
                        print(Lyric)

                # ONLY NOW update repeat counter!!
                repeat_counter = repeat_counter + self.RepeatedMeasureByVolta[currMeasureIndex]

                    # save transitions to file regardless of Lyrics
                    # if prevState != self.HarmonicStateMachine.getCadentialOutput().value:
                    #    print(f"{measuresSecondsMap[currMeasureIndex]['offsetSeconds']} {self.HarmonicStateMachine.getCadentialOutput().value}", file=text_fileTransitions)
                    # prevState = self.HarmonicStateMachine.getCadentialOutput().value
                    # thisChord.lyric = str("block ") + str(i)

                # === for debugging measure number problems
                #LyricPerBeat.append((1,str(currMeasureIndex)))
                # === for debugging key shifting
                #currKeyString = self.Top2Keys[0][0]
                #challengerKeyString = self.Top2Keys[1][0]
                #LyricPerBeat.append((1, f'{currKeyString} {self.CurrSmoothedInterpretations[currKeyString]}'))
                #LyricPerBeat.append((1, f'{challengerKeyString} {self.CurrSmoothedInterpretations[challengerKeyString]}'))

                # write coefs per measure for offline analysis
                coefs_per_measure.append(copy.deepcopy(self.CurrSmoothedInterpretations))

                Parts = CurrMeasuresNotes.recurse().getElementsByClass(m21.stream.Part)
                Lyrics_to_filter = ['CA', '{', '}'] # for filtering the display
                for thisLyric in LyricPerBeat:
                    if thisLyric[1] not in Lyrics_to_filter:
                        found = 0
                        for index in range(0, self.NumParts):
                            for thisNote in Parts[-1-index].flat.notesAndRests:  # adding lyric from last part up, assuming its the bass line
                                if thisNote.beat == thisLyric[0]:
                                    thisNote.lyric = thisLyric[1]
                                    found = 1
                                    break
                            if found == 1:
                                break

                #write corrected key at end of measure
                if self.KeyDetectionMode == CDKeyDetectionModes.KSWithSmoothingCadenceSensitive or self.KeyDetectionMode == CDKeyDetectionModes.KSWithSmoothing:
                    correctedKeyString = self.TopKeys[0][0]
                    correctedKey = m21.key.Key(correctedKeyString)
                    self.CorrectedKeyPerMeasure.append(correctedKey)
        except:
            print(f"Exception occurred on measure {measure_number}")
            raise

        for c in self.ChordStreamRestless.recurse().getElementsByClass('Chord'):
            c.closedPosition(forceOctave=4, inPlace=True)
        # this adds the restless chord stream to the note stream
        # self.NoteStream.insert(0, self.ChordStream)
        self.filter_notestream_by_language_model()
        self.filter_analysis_by_language_model()
        self.cleanup_lyrics(['{', '}'])
        self.write_analysis_to_files()

        if self.KeyDetectionMode == CDKeyDetectionModes.KSWithSmoothingCadenceSensitive or self.KeyDetectionMode == CDKeyDetectionModes.KSWithSmoothing:
            print("Writing cadence corrected keys to file...")
            keyfileName = self.fileName.replace(".", "_")
            FullPath = os.path.join(self.WritePath, keyfileName)
            KeyFile = f"{FullPath}_Key_{self.KeyDetectionMode}.txt"
            with open(KeyFile, 'wb') as f:
                pickle.dump(self.CorrectedKeyPerMeasure, f)
            CoefsFile = f"{FullPath}_Coefs_{self.KeyDetectionMode}.txt"
            with open(CoefsFile, 'wb') as f:
                pickle.dump(coefs_per_measure, f)

    def isilos(self, sub, list_or_string):
        if isinstance(list_or_string, list):
            ret_val = any(sub in s for s in list_or_string)
        else:
            ret_val = sub in list_or_string
        return ret_val

    def cleanup_lyrics(self, lyric_list):
        print('cleaning up lyrics')
        for part in self.Parts:
            for measure in part.recurse().getElementsByClass(m21.stream.Measure):
                for thisNote in measure.recurse().getElementsByClass(m21.note.GeneralNote):
                    for lyric in lyric_list:
                        thisNote.lyric = thisNote.lyric.replace(lyric, '')

    def filter_notestream_by_language_model(self):
        print('Filtering lyrics by language model...')
        PrevMeasureNotes = None
        PrevMeasureLyrics = None
        AnchorCadenceMeasureNumber = 0
        PrevParts = []
        empty_measure_counter = 0
        for currMeasureIndex in range(0, self.NumMeasures):
            if self.EmptyMeasures[currMeasureIndex]:
                empty_measure_counter = empty_measure_counter + 1
                continue
            measure_number = currMeasureIndex + 1
            CurrMeasureNotes = self.NoteStream.measure(measure_number)
            CurrParts = CurrMeasureNotes.recurse().getElementsByClass(m21.stream.Part)

            measure_number_for_score = measure_number - self.hasPickupMeasure - empty_measure_counter
            measures_since_anchor  = measure_number_for_score - AnchorCadenceMeasureNumber
            even_meas_since_anchor = measures_since_anchor % 2 == 0

            CurrMeasureLyrics = []
            for part in CurrParts:
                for thisNote in part.flat.notesAndRests:
                    CurrMeasureLyrics.append(thisNote.lyric)

            def remove_lyric_from_parts(lyric_list, parts):
                for part in parts:
                    for thisNote in part.flat.notesAndRests:
                        for lyric in lyric_list:
                            thisNote.lyric = thisNote.lyric.replace(lyric, '')

            if PrevMeasureNotes and PrevMeasureLyrics:
                # HC --> PAC
                if (self.isilos('HC', PrevMeasureLyrics) or self.isilos('PCH', PrevMeasureLyrics)) and (self.isilos('PAC', CurrMeasureLyrics) or self.isilos('PCC', CurrMeasureLyrics)):
                    remove_lyric_from_parts(['PCH'], PrevParts)
                    if even_meas_since_anchor or measures_since_anchor not in self.AnchorRange:
                        print(f'Filtering HC in measure {measure_number_for_score-1}')
                        remove_lyric_from_parts(['HC'], PrevParts)
                    #elif self.isilos('HC', PrevMeasureLyrics):
                    #    print(f'Filtering PAC in measure {measure_number_for_score}')
                    #    remove_lyric_from_parts(['PAC'], CurrParts)
                # PAC --> HC
                if self.isilos('PAC', PrevMeasureLyrics) and (self.isilos('HC', CurrMeasureLyrics) or self.isilos('PCH', CurrMeasureLyrics)):
                    remove_lyric_from_parts(['PCH'], CurrParts)
                    if not even_meas_since_anchor or measures_since_anchor not in self.AnchorRange:
                        print(f'Filtering HC in measure {measure_number_for_score}')
                        remove_lyric_from_parts(['HC'], CurrParts)
                # PAC + HC
                if (self.isilos('HC', CurrMeasureLyrics) or self.isilos('PCH', CurrMeasureLyrics)) and (self.isilos('PAC', CurrMeasureLyrics) or self.isilos('PCC', CurrMeasureLyrics)):
                    print(f'Filtering HC in measure {measure_number_for_score}')
                    remove_lyric_from_parts(['HC', 'PCH'], CurrParts)
                # HC --> IAC
                if (self.isilos('HC', PrevMeasureLyrics) or self.isilos('PCH', PrevMeasureLyrics)) and (self.isilos('IAC', CurrMeasureLyrics)):
                    remove_lyric_from_parts(['PCH'], PrevParts)
                    if even_meas_since_anchor or measures_since_anchor not in self.AnchorRange:
                        print(f'Filtering HC in measure {measure_number_for_score - 1}')
                        remove_lyric_from_parts(['HC'], PrevParts)
                    else:
                        print(f'Filtering IAC in measure {measure_number_for_score}')
                        remove_lyric_from_parts(['IAC'], CurrParts)
                # IAC --> HC
                if self.isilos('IAC', PrevMeasureLyrics) and (self.isilos('HC', CurrMeasureLyrics) or self.isilos('PCH', CurrMeasureLyrics)):
                    print(f'Filtering IAC in measure {measure_number_for_score - 1}')
                    remove_lyric_from_parts(['IAC'], PrevParts)
                # HC+IAC
                if (self.isilos('HC', CurrMeasureLyrics) or self.isilos('PCH', CurrMeasureLyrics)) and self.isilos('IAC', CurrMeasureLyrics):
                    print(f'Filtering IAC in measure {measure_number_for_score}')
                    remove_lyric_from_parts(['IAC'], CurrParts)
                # PAC+IAC
                if (self.isilos('PAC', CurrMeasureLyrics) or self.isilos('PCC', CurrMeasureLyrics)) and self.isilos('IAC', CurrMeasureLyrics):
                    print(f'Filtering IAC in measure {measure_number_for_score}')
                    remove_lyric_from_parts(['IAC'], CurrParts)
                # PAC --> IAC
                if (self.isilos('PAC', PrevMeasureLyrics) or self.isilos('PCC', PrevMeasureLyrics)) and self.isilos('IAC', CurrMeasureLyrics):
                    print(f'Filtering IAC in measure {measure_number_for_score}')
                    remove_lyric_from_parts(['IAC'], CurrParts)

            # get lyrics again after filtering
            CurrMeasureLyrics = []
            for part in CurrParts:
                for thisNote in part.flat.notesAndRests:
                    CurrMeasureLyrics.append(thisNote.lyric)
            PrevMeasureLyrics = []
            for part in PrevParts:
                for thisNote in part.flat.notesAndRests:
                    PrevMeasureLyrics.append(thisNote.lyric)

            # update anchor cadence from prev part
            anchor_cad_strings = ['PAC', 'PCC']
            if PrevMeasureLyrics and any(self.isilos(s, PrevMeasureLyrics) for s in anchor_cad_strings):
                AnchorCadenceMeasureNumber = measure_number_for_score - 1

            PrevMeasureNotes = CurrMeasureNotes
            PrevMeasureLyrics = CurrMeasureLyrics
            PrevParts = CurrParts


    def filter_analysis_by_language_model(self):
        print('Filtering analysis results by language model...')
        self.analysis_full_filtered = copy.deepcopy(self.analysis_full)
        items_to_remove = []
        prev_cad = {'Measure':0, 'Lyric':[]}
        anchor_cad = {'Measure':0, 'Lyric':[]}
        for item in self.analysis_full_filtered:
            curr_cad = item
            # check if cadence in analysis line
            cad_strings = ['PAC', 'PCC', 'HC', 'PCH', 'IAC']
            if not any(s in curr_cad['Lyric'] for s in cad_strings):
                continue
            measures_since_anchor = curr_cad['Measure'] - anchor_cad['Measure']
            even_meas_since_anchor = measures_since_anchor % 2 == 0
            if curr_cad['Measure'] - prev_cad['Measure'] <= 1:
                # HC --> PAC and HC+PAC
                if ('HC' in prev_cad['Lyric'] or 'PCH' in prev_cad['Lyric']) and ('PAC' in curr_cad['Lyric'] or 'PCC' in curr_cad['Lyric']):
                    if even_meas_since_anchor or measures_since_anchor not in self.AnchorRange or curr_cad['Measure'] == prev_cad['Measure']:
                        if prev_cad not in items_to_remove:
                            print(f"Filtering HC in measure {prev_cad['Measure']}")
                            items_to_remove.append(prev_cad)
                    #elif 'HC' in prev_cad['Lyric']:
                    #    if curr_cad not in items_to_remove:
                    #        print(f"Filtering PAC in measure {curr_cad['Measure']}")
                    #        items_to_remove.append(curr_cad)
                # PAC --> HC and PAC+HC
                if ('PAC' in prev_cad['Lyric'] or 'PCC' in prev_cad['Lyric']) and ('HC' in curr_cad['Lyric'] or 'PCH' in curr_cad['Lyric']):
                    if not even_meas_since_anchor or measures_since_anchor not in self.AnchorRange or curr_cad['Measure'] == prev_cad['Measure']:
                        if curr_cad not in items_to_remove:
                            print(f"Filtering HC in measure {curr_cad['Measure']}")
                            items_to_remove.append(curr_cad)
                # HC --> IAC
                if ('HC' in prev_cad['Lyric'] or 'PCH' in prev_cad['Lyric']) and 'IAC' in curr_cad['Lyric']:
                    if (even_meas_since_anchor or measures_since_anchor not in self.AnchorRange) and curr_cad['Measure'] > prev_cad['Measure']:
                        if prev_cad not in items_to_remove:
                            print(f"Filtering HC in measure {prev_cad['Measure']}")
                            items_to_remove.append(prev_cad)
                    else:
                        if curr_cad not in items_to_remove:
                            print(f"Filtering IAC in measure {curr_cad['Measure']}")
                            items_to_remove.append(curr_cad)
                # IAC --> HC
                if 'IAC' in prev_cad['Lyric'] and ('HC' in curr_cad['Lyric'] or 'PCH' in curr_cad['Lyric']):
                    if prev_cad not in items_to_remove:
                        print(f"Filtering IAC in measure {prev_cad['Measure']}")
                        items_to_remove.append(prev_cad)
                # IAC --> PAC
                if 'IAC' in prev_cad['Lyric'] and ('PAC' in curr_cad['Lyric'] or 'PCC' in curr_cad['Lyric']):
                    if prev_cad not in items_to_remove:
                        print(f"Filtering IAC in measure {prev_cad['Measure']}")
                        items_to_remove.append(prev_cad)
                # PAC --> IAC
                if 'IAC' in curr_cad['Lyric'] and ('PAC' in prev_cad['Lyric'] or 'PCC' in prev_cad['Lyric']):
                    if curr_cad not in items_to_remove:
                        print(f"Filtering IAC in measure {curr_cad['Measure']}")
                        items_to_remove.append(curr_cad)


            # update cadence only if not removed
            if curr_cad not in items_to_remove:
                if prev_cad not in items_to_remove:
                    # update anchor cadence only on PAC and HC
                    anchor_cad_strings = ['PAC', 'PCC']
                    if any(s in prev_cad['Lyric'] for s in anchor_cad_strings):
                        anchor_cad = prev_cad
                # update prev cad always
                prev_cad = curr_cad

        for item in items_to_remove:
            self.analysis_full_filtered = list(filter(lambda a: a != item, self.analysis_full_filtered))

    def write_analysis_to_files(self):
        fileName = self.fileName.replace(".", "_")
        FullPath = os.path.join(self.WritePath, fileName)
        text_file = open(f"{FullPath}_Analyzed.txt", "w")
        print(f"NumMeasures: {self.NumMeasures}", file=text_file)
        text_fileOffsets = open(f"{FullPath}_Analyzed_OffsetsNums.txt", "w")
        text_fileTransitions = open(f"{FullPath}_Analyzed_Transitions.txt", "w")

        for item in self.analysis_full_filtered:
            print(f"Measure: {item['Measure']} Offset: {item['Offset']} {item['Lyric']}", file=text_file)
            Lyric = item['Lyric']
            if "PAC" in Lyric:
                CadString = "PAC"
            elif "IAC" in Lyric:
                CadString = "IAC"
            elif "HC" in Lyric:
                CadString = "HC"
            elif "PCC" in Lyric:
                CadString = "PCC"
            elif "PCH" in Lyric:
                CadString = "PCH"
            CadStringToNumMap = {"PAC": CDCadentialStates.PACArrival.value, "IAC": CDCadentialStates.IACArrival.value,
                                 "HC": CDCadentialStates.HCArrival.value, "PCC": CDCadentialStates.PCCArrival.value,
                                 "PCH": CDCadentialStates.PCHArrival.value}
            print(f"{item['Measure']} {item['Offset']} {CadStringToNumMap[CadString]}", file=text_fileOffsets)

        for item in self.analysis_transition_strings:
            print(item, file=text_fileTransitions)

        text_file.close()
        text_fileOffsets.close()
        text_fileTransitions.close()

    def check_and_update_timesig(self, CurrMeasures, measure_time_sig):
        if CurrMeasures:
            for timeSig in CurrMeasures.recurse().getElementsByClass(m21.meter.TimeSignature):
                measure_time_sig = timeSig
                if timeSig != self.HarmonicStateMachine.CurrHarmonicState.TimeSig:
                    self.HarmonicStateMachine.CurrHarmonicState.TimeSig = timeSig
                    self.HarmonicStateMachineChallenger1.CurrHarmonicState.TimeSig = timeSig
                    self.HarmonicStateMachineChallenger2.CurrHarmonicState.TimeSig = timeSig
        return measure_time_sig

    def getSubDominantPitchClass(self, currKey):
        return (currKey.getDominant().pitchClass - 2) % 12

    def updateKeysAndSwapStateMachines(self, currKeyString, challenger1KeyString, challenger2KeyString):
        # this swap assures the smoothness of key transition if challenger becomes main (and main becomes challenger)
        if currKeyString != self.PrevKeyString:
            tempStateMachine = copy.deepcopy(self.HarmonicStateMachine)
            if currKeyString == self.PrevChallenger1KeyString:
                self.HarmonicStateMachine = copy.deepcopy(self.HarmonicStateMachineChallenger1)
                self.HarmonicStateMachine.CadentialKeyChange = 1
            if currKeyString == self.PrevChallenger2KeyString:
                self.HarmonicStateMachine = copy.deepcopy(self.HarmonicStateMachineChallenger2)
                self.HarmonicStateMachine.CadentialKeyChange = 1
            if challenger1KeyString == self.PrevKeyString:
                self.HarmonicStateMachineChallenger1 = copy.deepcopy(tempStateMachine)
            if challenger2KeyString == self.PrevKeyString:
                self.HarmonicStateMachineChallenger2 = copy.deepcopy(tempStateMachine)
            # reset post cadential counters
            if not self.CadentialKeyChange:
                self.HarmonicStateMachine.resetPostCadentialCounters()
            self.HarmonicStateMachineChallenger1.resetPostCadentialCounters()
            self.HarmonicStateMachineChallenger2.resetPostCadentialCounters()
        self.PrevKeyString = currKeyString
        self.PrevChallenger1KeyString = challenger1KeyString
        self.PrevChallenger2KeyString = challenger2KeyString
        self.HarmonicStateMachine.IsChallenger = False
        self.HarmonicStateMachineChallenger1.IsChallenger = True
        self.HarmonicStateMachineChallenger2.IsChallenger = True

    def setFileName(self,fileName):
        self.fileName = fileName

    def display(self):
        # open in MuseScore
        self.ChordStream.show()

    def writeAnalyzedFile(self):
        max_num_measures_for_writing = 400
        if self.NumMeasures <= max_num_measures_for_writing:
            fileName = self.fileName.replace(".", "_")
            fileName = (f"{fileName}_Analyzed.xml")
            FullPath = os.path.join(self.WritePath, fileName)
            self.NoteStream.write(fp=FullPath)
        else:
            print(f'file too long for writing. Max num measures for writing is {max_num_measures_for_writing}.'
                  f'Num measures is:', self.NumMeasures)

    def displayFull(self):
        self.NoteStream.show()

    def setWritePath(self,path):
        self.WritePath = path
