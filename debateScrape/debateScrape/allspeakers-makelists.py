import json

with open('allSpeakersBackup.json', 'r') as f:
    allSpeakerBackup = json.load(f)

allSpeakerOut = []

for debate in allSpeakerBackup:
    debateOut = {}
    debateOut['date'] = debate['date']
    debateOut['description'] = debate['description']
    debateOut['speakerLists'] = []
    for speaker in debate['speakers']:
        if 'identity' not in speaker:
            speakerList = [speaker['name']]
            for speaker2 in debate['speakers']:
                if 'identity' in speaker2:
                    if speaker2['identity'] == speaker['name']:
                        speakerList.append(speaker2['name'])
            debateOut['speakerLists'].append(speakerList)
    allSpeakerOut.append(debateOut)

    # Check that all the speakers are now included in the lists:

    for speakerNameIDPair in debate['speakers']:
        if not [True for speakerList in debateOut['speakerLists'] if speakerNameIDPair['name'] in speakerList]:
            print speakerNameIDPair['name']
            for speakerList in debateOut['speakerLists']:
                print speakerList


with open('allSpeakersOut.json', 'w') as f:
    json.dump(allSpeakerOut,f)