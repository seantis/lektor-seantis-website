/*
Tipue Search 5.0
Copyright (c) 2015 Tipue
Tipue Search is released under the MIT License
http://www.tipue.com/search
*/

/* Stop words list from http://www.ranks.nl/stopwords/german */
var tipuesearch_stop_words = ["aber", "als", "am", "an", "auch", "auf", "aus", "bei", "bin", "bis", "bist", "da", "dadurch", "daher", "darum", "das", "daß", "dass", "dein", "deine", "dem", "den", "der", "des", "dessen", "deshalb", "die", "dies", "dieser", "dieses", "doch", "dort", "du", "durch", "ein", "eine", "einem", "einen", "einer", "eines", "er", "es", "euer", "eure", "für", "hatte", "hatten", "hattest", "hattet", "hier", "hinter", "ich", "ihr", "ihre", "im", "in", "ist", "ja", "jede", "jedem", "jeden", "jeder", "jedes", "jener", "jenes", "jetzt", "kann", "kannst", "können", "könnt", "machen", "mein", "meine", "mit", "muß", "mußt", "musst", "müssen", "müßt", "nach", "nachdem", "nein", "nicht", "nun", "oder", "seid", "sein", "seine", "sich", "sie", "sind", "soll", "sollen", "sollst", "sollt", "sonst", "soweit", "sowie", "und", "unser", "unsere", "unter", "vom", "von", "vor", "wann", "warum", "was", "weiter", "weitere", "wenn", "wer", "werde", "werden", "werdet", "weshalb", "wie", "wieder", "wieso", "wir", "wird", "wirst", "wo", "woher", "wohin", "zu", "zum", "zur", "über"];

var tipuesearch_replace = {'words': []};
var tipuesearch_weight = {'weight': []};
var tipuesearch_stem = {'words': []};

var tipuesearch_string_1 = 'Kein Title';
var tipuesearch_string_2 = 'Resultate für';
var tipuesearch_string_3 = 'Suche stattdessen nach';
var tipuesearch_string_4 = '1 Resultat';
var tipuesearch_string_5 = 'Resultate';
var tipuesearch_string_6 = 'Vorherige';
var tipuesearch_string_7 = 'Nächste';
var tipuesearch_string_8 = 'Nichts gefunden.';
var tipuesearch_string_9 = 'Häufig verwendete Begriffe werden weitgehend ignoriert';
var tipuesearch_string_10 = 'Suchbegriff zu kurz';
var tipuesearch_string_11 = 'Sollte mindestens ein Zeichen sein';
var tipuesearch_string_12 = 'Sollte';
var tipuesearch_string_13 = 'Zeichen oder mehr';
