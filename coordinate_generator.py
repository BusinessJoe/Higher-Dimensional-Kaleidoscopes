import numpy as np

# For some reason, with these settings the correct output isn't made? Maybe?

# The coxeter diagram encoded as numbers
# The first column represents the dihedral angle
# The second column represents which nodes are "active"



def generateNormals(diag, dim):
    output = np.zeros((dim, dim))
    output[0][0] = 1

    for i in range(1, dim):
        for j in range(i + 1):
            if j + 2 <= i:
                output[i][j] = 0
            elif j + 1 <= i:
                output[i][j] = np.cos(np.pi / diag[i - 1][0]) / output[i - 1][j]
            else:
                output[i][j] = np.sqrt(1 - np.square(output[i][j - 1]))
    return output


def normalReflection(point, normal):
    return [point - 2 * np.dot(point, normal) * normal]


def removeDoubles(point):
    return np.unique(np.round(point, 5), axis=0)


def generateStartPoint(normalValues, activationValues):
    print(normalValues)
    print(activationValues)
    genPoint = np.linalg.solve(normalValues, activationValues)
    print(genPoint)
    print(np.allclose(np.dot(normalValues, genPoint), activationValues))
    return np.array([genPoint])


def generatePointsFromDiagram(diagram, dimension, iterations):
    normals = generateNormals(diagram, dimension)

    points = generateStartPoint(normals, np.array(diagram)[:, 1])
    #points = np.array([[0, 1.414, 0.1]])
    for iteration in range(iterations):
        for d in range(dimension):
            for p in range(len(points)):
                reflected_points = normalReflection(points[p], normals[d])
                points = np.concatenate((points, reflected_points))

            points = removeDoubles(points)
    return points
