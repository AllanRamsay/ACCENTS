The GALE data comes in two pieces -- the recordings and the
transcripts.

The transcripts consist of a set of files with names like
ALJZ_MOREOPINION1_ARB_20070428_055800.qrtr.tdf, where the content of a
file looks like

ALJZ_MOREOPINION1_ARB_20070428_055800   0       96.4965517241   104.706592138   speaker1        male    native  إستشهاد أربعة فلسطينيين من كتائب القسام بنيران قوات الاحتلال قرب الحدود شرق مدينة غزة     2       0       1       report  statement
ALJZ_MOREOPINION1_ARB_20070428_055800   0       107.172413793   116.275862069   speaker1        male    native  الجيش التركي يحذر بشدة من محاولة المساس بالعلمانية وأوروبا تطالبه باحترام العملية الديمقراطية   2       0       3       report  statement
...

The signature for a line from this file is

file;unicode    channel;int     start;float     end;float       speaker;unicode speakerType;unicode     speakerDialect;unicode  transcript;unicode      section;int     turn;int        segment;int     sectionType;unicode     suType;unicode

where file is the name of the transcription file and also of the
recording that it is a transcription of; channel is the recording
channel; start and end are the time stamps for this section of the
file; speaker, speakerType, speakerDialect tell you things about the
speaker (the dialect is simply native/nonnative, so is *not* what we
use in our experiments); transcript is the actual transcription (which
is undiacriticised); the other bits tell you things about the segment,
but they're not things that we make use of.

The original recordings are quite long, typically about
an hour. For our experiments we split the original recordings into
segments, corresponding to the time stamps in the transcription. Our
experiments are all done on these segments. To get them, we use a
couple of python scripts (we use Python2.7; these scripts could fairly
easily be rewritten to Python3, but the ones that drive the main
experiments (which are *not* included here) would take a lot of work,
so we just use 2.7 for everything).

**********************************************************************
flac2wav.py; the recordings are distributed as .flac files. We find it
easier to work with .wav files, so we need to convert the .flac files
to .wav. There are probably loads of things that will do this; we use
the Unix ffmpeg utility, wrapped up in a script called
flac2wav.py. This is called with two arguments, the location where the
.flac files are stored (which will typically be a directory with a
name like gale_p3_bn_speech_p1/data (for broadcast news) or
gale_p3_bnc_speech_p1/data (for broadcast speech)) and the location
where we want the wav files to go (usually gale_p3_bn_speech_p1/wav or
gale_p3_bc_speech_p1/wav).

$ ./flac2wav.py src=gale_p3_bn_speech_p1/data dest=gale_p3_bn_speech_p1/wav

(make sure you've got lots of space -- there are several hundred hours
of recordings in these files, so they take up quite a bit work)

**********************************************************************
segments.py; once we've got the original recordings as .wav files, we
need to split them into segments. We want several things out of this:
the transcription for each segment, the section of the recording
covering the period in the time stamp for the segment, maybe the
Buckwalter transliteration of the transcription, maybe the Madamira
output for the transcription. segments.py has flags that control which
of these you get (you can only get the Madamira output if you've
downloaded Madamira and the SAMA, getting the recordings is a bit time
consuming so you might not want to do it more than once, ...). Again
you have to say where the original transcriptions and wav files are
stored and where you want the results to go;

./segments.py src=gale_p3_ara_bn_transcripts_p1/data/tdf wav=gale_p3_bn_speech_p1/wav runMadamira=1 copywavfiles=1 dest=TEMP

TEMP will now contain lots of files with names like
ARABIYA_LATEHRNEWS_ARB_20070227_000000, which themselves contain a set
of files called

originalprompts.segments		originalprompts.segments.bw
originalprompts.segments.ATB.tok	originalprompts.segments.mada

These contain the original prompts from
ARABIYA_LATEHRNEWS_ARB_20070227_000000, the Buckwalter version of
these, and the Madamira output for them (assuming that you have
Madamira installed, otherwise this obviously won't work)

There will also be folder called TEMP/wav which contains the .wav
files for each of these segments.



