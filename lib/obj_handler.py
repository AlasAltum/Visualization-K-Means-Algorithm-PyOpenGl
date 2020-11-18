from lib.basic_shapes import Shape as _Shape


def readFaceVertex(faceDescription):

    aux = faceDescription.split("/")

    assert len(aux[0]), "Vertex index has not been defined."

    faceVertex = [int(aux[0]), None, None]

    assert len(aux) == 3, "Only faces where its vertices require 3 indices are defined."

    if len(aux[1]) != 0:
        faceVertex[1] = int(aux[1])

    if len(aux[2]) != 0:
        faceVertex[2] = int(aux[2])

    return faceVertex


def readOBJ(filename, color):

    vertices = []
    normals = []
    texCoords = []
    faces = []

    with open(filename, "r") as file:
        for line in file.readlines():
            aux = line.strip().split(" ")

            if aux[0] == "v":
                vertices += [[float(coord) for coord in aux[1:]]]

            elif aux[0] == "vn":
                normals += [[float(coord) for coord in aux[1:]]]

            elif aux[0] == "vt":
                assert (
                    len(aux[1:]) == 2
                ), "Texture coordinates with different than 2 dimensions are not supported"
                texCoords += [[float(coord) for coord in aux[1:]]]

            elif aux[0] == "f":
                N = len(aux)
                faces += [[readFaceVertex(faceVertex) for faceVertex in aux[1:4]]]
                for i in range(3, N - 1):
                    faces += [
                        [
                            readFaceVertex(faceVertex)
                            for faceVertex in [aux[i], aux[i + 1], aux[1]]
                        ]
                    ]

        vertexData = []
        indices = []
        index = 0

        # Per previous construction, each face is a triangle
        for face in faces:

            # Checking each of the triangle vertices
            for i in range(0, 3):
                vertex = vertices[face[i][0] - 1]
                normal = normals[face[i][2] - 1]

                vertexData += [
                    vertex[0],
                    vertex[1],
                    vertex[2],
                    color[0],
                    color[1],
                    color[2],
                    normal[0],
                    normal[1],
                    normal[2],
                ]

            # Connecting the 3 vertices to create a triangle
            indices += [index, index + 1, index + 2]
            index += 3

        return _Shape(vertexData, indices)


def readTextureOBJ(filename, texfilename):

    vertices = []
    normals = []
    texCoords = []
    faces = []

    with open(filename, "r") as file:
        for line in file.readlines():
            aux = line.strip().split(" ")

            if aux[0] == "v":
                vertices += [[float(coord) for coord in aux[1:]]]

            elif aux[0] == "vn":
                normals += [[float(coord) for coord in aux[1:]]]

            elif aux[0] == "vt":
                assert (
                    len(aux[1:]) == 2
                ), "Texture coordinates with different than 2 dimensions are not supported"
                texCoords += [[float(coord) for coord in aux[1:]]]

            elif aux[0] == "f":
                N = len(aux)
                faces += [[readFaceVertex(faceVertex) for faceVertex in aux[1:4]]]
                for i in range(3, N - 1):
                    faces += [
                        [
                            readFaceVertex(faceVertex)
                            for faceVertex in [aux[i], aux[i + 1], aux[1]]
                        ]
                    ]

        vertexData = []
        indices = []
        index = 0

        # Per previous construction, each face is a triangle
        for face in faces:

            # Checking each of the triangle vertices
            for i in range(0, 3):
                vertex = vertices[face[i][0] - 1]
                texture = texCoords[face[i][1] - 1]
                normal = normals[face[i][2] - 1]

                vertexData += [
                    vertex[0],
                    vertex[1],
                    vertex[2],
                    texture[0],
                    texture[1],
                    normal[0],
                    normal[1],
                    normal[2],
                ]

            # Connecting the 3 vertices to create a triangle
            indices += [index, index + 1, index + 2]
            index += 3

        return _Shape(vertexData, indices, texfilename)
