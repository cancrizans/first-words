# -*- coding: UTF-8 -*-
IPAsubs = {
#	Syllabic m
	"mm"				:"uũ",
	"mʼm"				:"ṵʼũ",
	r"([aàeèiìoòuù])m([^aàeèiìoòuùm]|$)"	:r"\1ũ\2" ,
#	Clicks
	"ʇ"					:"ǀ"	,
	r"[nɴ]([ʘǀǁǂǃ])x"		:r"ᵑ\1͡ʁ" ,
	r"([ʘǀǁǂǃ])x"		:r"\1͡χ"	,
	r"[nɴ]([ʘǀǁǂǃ])"		:r"ᵑ\1" ,
	r"([ʘǀǁǂǃ])qʼ"		:r"\1͡qE",
	r"([ʘǀǁǂǃ])ʼ"		:r"\1ˀ" ,
	r"ʛ"				:r"͡ʛ6"	,
	"sǀ"				:"s̪ǀ"	,
	r"[sṣ]ǂ"			:"ʂǂ"	,
	r"[sš]ǃ"			:"ʃǃ"	,
	r"[sšł]ǁ"			:"ɬǁ"	,
#	Ejectives
	r"([ṭłqc])ʼ"		:r"\1E" ,
#	Pulmonics unaffected
	"tš"				:"č"	,
	"ṭ"					:"ʈ"    ,
	"tł"				:"L"	,
	"ʼ"					:"ʔ"	,
	"ṇ"					:"ɳ"	,
	"n"					:"n̪"	,
	"ň"					:"ɲ"	,
	"ñ"					:"ɲ"	,
	"č"					:"C"	,
	"ts"				:"D"	,
	"ṯ"					:"D"	,
	"tṣ"				:"ʈ͡ʂ"	,
	"t"					:"D"	,
	"j"					:"ɟ"	,
#	Fix ejective, dental affricate
	"E"					:"ʼ"	,
	"D"					:"t͡s̪"	,
	"C"					:"t͡ʃ"	,
	"L"					:"t͡ɬ"	,
# 	Vowel segment unrolling
	"([aeiou])̰"			:r"C\1" ,
	"ḛ"					:r"Ce"	,
	"ḭ"					:r"Ci"	,
	"ṵ"					:r"Cu"	,
	"à"					:"Ca"	,
	"è"					:"Ce"	,
	"ì"					:"Ci"	,
	"ò"					:"Cɔ"	,
	"ù"					:"Cu"	,
	"ã"					:"aN"	,
	"ẽ"					:"eN"	,
	"ĩ"					:"iN"	,
	"õ"					:"ɔN"	,
	"ũ"					:"uN"	,
	"o"					:"ɔ"	,
#	syllabic m detection
	r"m([^aeiɔouC]|\b)"	:"uN"	,

# 	broken nasal phonation
	r"C([aeiɔou])ʔ\1N" 	:r"C\1Nʔ\1N",

#	Monophthongize
	r"([aeiɔu])\1"		:r"\1ː"	,
#	Bring nasal in
	"ːN"				:"Nː"	,
#	Pre-nasal click nasality
	r"([aeiɔu])ᵑ"		:r"\1Nᵑ",
#	Dupe for diphthongs
	r"(C?)([aeiɔu])([aeiɔu])(N?)" : r"\1\2\4\1\3\4",
#	Creaky-Nasal fix
	r"C([aeiɔu]N)"		:r"\1̰",
#	Nasalize
	"aN"				:"ã"	,
	"eN"				:"ẽ"	,
	"ɔN"				:"ɔ̃"	,
	"iN"				:"ĩ"	,
	"uN"				:"m"	,
#	Creaky
	r"C([aeiɔu])"		:r"\1̰" 	,


}


lowercase_subs = {
	"Ʇ":"ʇ"
}

import re

def superLowerCase(text):
	text = text.lower()
	for patt in lowercase_subs:
		text = text.replace(patt, lowercase_subs[patt])
	return text

def log(s,resetLog=False):
	with open("pronunciatorlog.txt",'w' if resetLog else 'a',encoding="utf-8") as f:
		f.write(s+"\n")

def pronunciate(text, debug=False):
	if debug:
		log("",True)
	text = superLowerCase(text)

	for patt in IPAsubs:
		repl = IPAsubs[patt]


		text = re.sub(patt,repl,text)

		if debug:
			log(text)

	return text


if __name__ == "__main__":

	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("--test", help="input text for pronunciation")
	#parser.add_argument("--silent",  help="input text for pronunciation")

	args = parser.parse_args()

	if(args.test):
		pron = pronunciate(args.test,False)
		print(pron)

