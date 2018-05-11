accents.sql contains the annotations described in "The development of
a speech corpus annotated for the main Arabic dialects", Eiman
Alsharhan & Allan Ramsay. There are three tables:

ACCENTS;
+-----------+--------------+------+-----+---------+-------+
| Field     | Type         | Null | Key | Default | Extra |
+-----------+--------------+------+-----+---------+-------+
| speaker   | varchar(255) | YES  |     | NULL    |       |
| accent    | varchar(255) | YES  |     | NULL    |       |
| annotator | varchar(255) | YES  |     | NULL    |       |
+-----------+--------------+------+-----+---------+-------+

Each row in ACCENTS corresponds to a single annotation, where
annotator has marked speaker as having accent.

SPEAKERS;
+-------+--------------+------+-----+---------+-------+
| Field | Type         | Null | Key | Default | Extra |
+-------+--------------+------+-----+---------+-------+
| name  | varchar(255) | YES  |     | NULL    |       |
| count | int(11)      | YES  |     | 0       |       |
+-------+--------------+------+-----+---------+-------+

SPEAKERS is just a list of speaker names. The count is a dummy field
which contains 0 for every speaker;

RECORDINGS;
+---------+--------------+------+-----+---------+-------+
| Field   | Type         | Null | Key | Default | Extra |
+---------+--------------+------+-----+---------+-------+
| speaker | varchar(255) | YES  |     | NULL    |       |
| file    | varchar(255) | YES  |     | NULL    |       |
+---------+--------------+------+-----+---------+-------+

RECORDINGS links speakers to the files that contain their utterances:
a single speaker will typically have several recordings. The
recordings themselves are the GALE recordings split into short split
into segments, where each file corresponds to a time-stamped segment
from one of the GALE files. The GALE data itself is provided through
the LDC -- we cannot distribute this data.

...
test-ALAM_IRAQNOW_ARB_20070802_092801-male-speaker3 | ../../NEWACCENTS/wav/test-ALAM_IRAQNOW_ARB_20070802_092801-male-speaker3-native-5.wav  
test-ALAM_IRAQNOW_ARB_20070802_092801-male-speaker3 | ../../NEWACCENTS/wav/test-ALAM_IRAQNOW_ARB_20070802_092801-male-speaker3-native-6.wav
...                                           |
