cvsInputFile = open("updated_diabetic_data.csv", "r")
cvsInputInformation = cvsInputFile.read()
cvsInputFile.close()
cvsInputStrings = cvsInputInformation.split("\n")
labels = cvsInputStrings[0].split(",")
cvsInputStrings.__delitem__(0)
cvsInputStrings.__delitem__(cvsInputStrings.__len__() - 1)
cvsInputRows = []
for i in range(0, cvsInputStrings.__len__()):
    cvsInputRows.append([])
    cvsInputRows[i] = cvsInputStrings[i].split(",")

cvsOutputRows = []
invalidEntries = []
for i in range(0, cvsInputStrings.__len__()):
    cvsOutputRows.append([])

    race = cvsInputRows[i][0]
    # Caucasian is 0, african american is 1, asian is 2, hispanic is 3, other/unknown is 4
    if race == "Caucasian":
        cvsOutputRows[i].append(0)
    elif race == "AfricanAmerican":
        cvsOutputRows[i].append(1)
    elif race == "Asian":
        cvsOutputRows[i].append(2)
    elif race == "Hispanic":
        cvsOutputRows[i].append(3)
    elif race == "?" or race == "Other":
        cvsOutputRows[i].append(4)

    gender = cvsInputRows[i][1]
    # If male 1, if female -1
    if gender == "Male":
        cvsOutputRows[i].append(1)
    elif gender == "Female":
        cvsOutputRows[i].append(-1)
    else:
        cvsOutputRows[i].append("?")
        invalidEntries.append(i)

    ageRange = cvsInputRows[i][2]
    minAge = ageRange[1:ageRange.index("-")]
    maxAge = ageRange[ageRange.index("-") + 1:ageRange.index(")")]
    cvsOutputRows[i].append(minAge)
    cvsOutputRows[i].append(maxAge)

    for j in range(3, 13):
        cvsOutputRows[i].append(cvsInputRows[i][j])

    for j in range(13, 16):
        diagnosis = cvsInputRows[i][j]
        if diagnosis.find(".") != -1:
            # if it's a length of 5 then that means it's in the form of 250.83 which means it's related to diabetes
            # diabetes will be given the id number 3
            cvsOutputRows[i].append(3)
        elif diagnosis[0].isalpha() or diagnosis[0] == '?':
            # If the first character is a letter than it is in the same form as a V57 classification
            # this means that it will be classified as other, other will be given the id number 8
            cvsOutputRows[i].append(8)
        else:
            # Now that we've simplified it down to only 3 digit numbers we can finish the classifications here
            diagnosis = int(diagnosis)
            if (diagnosis >= 390 and diagnosis <= 459) or diagnosis == 785:
                # Diagnosis is a circulatory problem, circulatory problems will be given the id 0.
                cvsOutputRows[i].append(0)
            elif (diagnosis >= 460 and diagnosis <= 519) or diagnosis == 786:
                # Diagnosis is a respiratory problem, respiratory problems will be given the id 1.
                cvsOutputRows[i].append(1)
            elif (diagnosis >= 520 and diagnosis <= 579) or diagnosis == 787:
                # Diagnosis is a digestive problem, digestive problems will be given the id 2.
                cvsOutputRows[i].append(2)
            elif diagnosis >= 800 and diagnosis <= 999:
                # Diagnosis is a injury or poisoning, these problems will be given the id 4
                cvsOutputRows[i].append(4)
            elif diagnosis >= 710 and diagnosis <= 739:
                # Diagnosis is a musculoskeletal problem these problems will be given the id 5.
                cvsOutputRows[i].append(5)
            elif (diagnosis >= 580 and diagnosis <= 629) or diagnosis == 788:
                # Diagnosis is a genitourinary issue, these problems will be given the id 6.
                cvsOutputRows[i].append(6)
            elif diagnosis >= 140 and diagnosis <= 239:
                # Diagnosis is a neoplasm issue, these problems will be given the id 7.
                cvsOutputRows[i].append(7)
            else:
                # These issues are classified as other, other is given the classification 8
                cvsOutputRows[i].append(8)


    cvsOutputRows[i].append(cvsInputRows[i][16])

    maxGluSerum = cvsInputRows[i][17]
    # if maxGluSerum is None, append 0, if it's norm append 1, if >200 it's 2, if >300 it's 3
    if maxGluSerum[0] == '>':
        cvsOutputRows[i].append(maxGluSerum[2:3])
    elif maxGluSerum == "None":
        cvsOutputRows[i].append(0)
    elif maxGluSerum == "Norm":
        cvsOutputRows[i].append(1)

    A1Cresult = cvsInputRows[i][18]
    # If none add 0, if norm add 1, if >7 add 7, if >8 add 8.
    if A1Cresult == "None":
        cvsOutputRows[i].append(0)
    elif A1Cresult == "Norm":
        cvsOutputRows[i].append(1)
    else:
        cvsOutputRows[i].append(A1Cresult[1:])

    # For values 19-42 they all have the same possible values.
    # No is 0, steady is 1, up is 2, down is 3
    for j in range(19, 42):
        value = cvsInputRows[i][j]
        if value == "No":
            cvsOutputRows[i].append(0)
        elif value == "Steady":
            cvsOutputRows[i].append(1)
        elif value == "Up":
            cvsOutputRows[i].append(2)
        elif value == "Down":
            cvsOutputRows[i].append(3)

    change = cvsInputRows[i][42]
    # If there is no change it's -1, if there is it is 1
    if change == 'No':
        cvsOutputRows[i].append(-1)
    elif change == "Ch":
        cvsOutputRows[i].append(1)

    diabetesMed = cvsInputRows[i][43]
    # If they use medication it's 1 if they don't it's -1
    if diabetesMed == "Yes":
        cvsOutputRows[i].append(1)
    elif diabetesMed == "No":
        cvsOutputRows[i].append(-1)

    readmitted = cvsInputRows[i][44]
    # If readmitted it will be 1, and if it's not it will be -1
    if readmitted == "1":
        cvsOutputRows[i].append(1)
    elif readmitted == "0":
        cvsOutputRows[i].append(-1)

# getting rid of invalid entries
for i in range(invalidEntries.__len__() - 1, -1, -1):
    cvsOutputRows.__delitem__(invalidEntries[i])

# inserting the labels for all of the things.
labels[2] = "min age"
labels.insert(3, "max age")
cvsOutputRows.insert(0, labels)

finalOutput = ""
for i in range(0, cvsOutputRows.__len__()):
    thisLine = ""
    for j in range(0, cvsOutputRows[i].__len__()):
        thisLine += str(cvsOutputRows[i][j]) + ","
    thisLine = thisLine[0:thisLine.__len__() - 1] + '\n'
    finalOutput += thisLine

outputFile = open("output.csv", "w")
outputFile.write(finalOutput)
outputFile.close()