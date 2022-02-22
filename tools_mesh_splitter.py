def detect_and_split_mesh(filename):

    filelist = []
    fi = open(filename,'r',encoding='utf8')
    objectname = ''
    newobj = "# XMU music robot"
    counter = 0
    v = 0
    vt = 0
    vn = 0
    x = 0
    y = 0
    z = 0
    last_v = 0
    last_vt = 0
    last_vn = 0
    centroid = []

    for line in fi:
        if 'mtl' in line or line[0] == '#': continue

        if line == 'g default\n': 
            if counter >= 1:
                #fo = open(directory + '/' + objectname + '.obj', 'w', encoding='utf8')
                fo = open(objectname + '.obj','w',encoding='utf8')
                filelist.append(objectname)
                objectname = ''
                fo.write(newobj)
                fo.close()
                newobj = "# XMU music robot\n"
                centroid.append([round(x/(v - last_v),5), round(z/(v - last_v),5), round(y/(v - last_v),5)])
                x = 0
                y = 0
                z = 0
                last_v = v
                last_vn = vn
                last_vt = vt

            counter += 1

        if line[0] == 'g' and 'default' not in line: objectname = line[2:-1]

        if line[0:2] == 'v ':
            v += 1
            number = ''
            xyzcounter = 0
            for char in line:
                if char == ' ':
                    if xyzcounter == 1:
                        x += float(number)
                    elif xyzcounter == 2:
                        y += float(number)
                    xyzcounter += 1
                    number = ''

                elif char != 'v':
                    number += char
            z += float(number)

        elif line[0:2] == 'vt':
            vt += 1
        elif line[0:2] == 'vn':
            vn += 1

        if line[0] == 'f':
            vector_count = 0
            number = ''
            temp_number = 0
            for char in line:

                if number != '' and (char == ' ' or char == '/'):
                    if vector_count % 3 == 0:
                        temp_number = int(number) - last_v
                    elif vector_count % 3 == 1:
                        temp_number = int(number) - last_vt
                    elif vector_count % 3 == 2:
                        temp_number = int(number) - last_vn

                    vector_count += 1
                    newobj += str(temp_number)
                    number = ''

                if char == 'f' or char == ' ' or char == '/':
                    newobj += char
                else:
                    number += char

            vector_count += 1
            temp_number = int(number) - last_vn
            newobj += str(temp_number)
            newobj += '\n'

        else:
            newobj += line

    #fo = open(directory + '/' + objectname + '.obj', 'w',encoding='utf8')
    fo = open(objectname + '.obj','w',encoding='utf8')
    filelist.append(objectname)
    centroid.append([round(x/(v - last_v),5), round(z/(v - last_v),5), round(y/(v - last_v),5)])
    fo.write(newobj)
    fo.close()
    filelist.append(centroid)
    filelist.append(counter)
    return filelist


#detect_and_split_mesh('double_spheres.obj','blah')