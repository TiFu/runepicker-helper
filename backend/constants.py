styles = [8000, 8100, 8200, 8300, 8400]
lanes = ["MARKSMEN", "SUPPORT", "MIDDLE", "TOP", "JUNGLE"]
styleNames = {
    8000: "precision",
    8100: "domination",
    8200: "sorcery",
    8300: "inspiration",
    8400: "resolve"
}
runesByPrimaryStyle = {
    8000: [
        [8005, 8008, 8021],
        [9101, 9111, 8009],
        [9104, 9105, 9103],
        [8014, 8017, 8299]
    ],
    8100: [
        [8112, 8124, 8128],
        [8126, 8139, 8143],
        [8136, 8120, 8138],
        [8135, 8134, 8105]
    ],
    8200: [
        [8214, 8229, 8230],
        [8224, 8226, 8243],
        [8210, 8234, 8233],
        [8237, 8232, 8236]
    ],
    8300: [
        [8326, 8351, 8359],
        [8306, 8345, 8313],
        [8304, 8321, 8316],
        [8347, 8410, 8339]        
    ],
    8400: [
        [8437, 8439, 8465],
        [8242, 8446, 8463],
        [8430, 8435, 8429],
        [8451, 8453, 8444]        
    ]
}

runesBySubStyle = {
    8000: set().union(*(runesByPrimaryStyle[8000][1:4])),
    8100: set().union(*(runesByPrimaryStyle[8100][1:4])),
    8200: set().union(*(runesByPrimaryStyle[8200][1:4])),
    8300: set().union(*(runesByPrimaryStyle[8300][1:4])),
    8400: set().union(*(runesByPrimaryStyle[8400][1:4]))
}