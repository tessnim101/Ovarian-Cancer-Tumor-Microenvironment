def path = '/Users/cynthiarabay/Desktop/hackathon3/im2/expression_calls_for_qupath.tsv'
def markerName = 'Cytokeratin'
def exprColumn = markerName + '_expr'

def lines = new File(path).readLines()
def header = lines[0].split('\t')

int objectIdIdx = header.findIndexOf { it == 'Object ID' }
int exprIdx = header.findIndexOf { it == exprColumn }

if (objectIdIdx < 0 || exprIdx < 0) {
    print 'Could not find Object ID or marker column'
    return
}

def callMap = [:]

lines.drop(1).each { line ->
    def parts = line.split('\t', -1)
    if (parts.size() > Math.max(objectIdIdx, exprIdx)) {
        callMap[parts[objectIdIdx]] = parts[exprIdx]
    }
}

def detections = getDetectionObjects()

detections.each { det ->
    def id = det.getID()?.toString()
    if (id != null && callMap.containsKey(id)) {
        def call = callMap[id]
        if (call == 'YES') {
            det.setPathClass(getPathClass(markerName + "_POS"))
        } else {
            det.setPathClass(getPathClass(markerName + "_NEG"))
        }
    }
}

fireHierarchyUpdate()
print "Done"