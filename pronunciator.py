IPAsubs = {
#	Clicks
	"ʇ"					:"ǀ"	,
	r"n([ǀǁǂǃ])x"		:r"ᵑ\1͡ʁ" ,
	r"([ǀǁǂǃ])x"		:r"\1͡χ"	,
	r"n([ǀǁǂǃ])"		:r"ᵑ\1" ,
	r"([ǀǁǂǃ])qʼ"		:r"\1͡qE",
	r"([ǀǁǂǃ])ʼ"		:r"\1ˀ" ,
	"sǀ"				:"s̪ǀ"	,
	r"[sṣ]ǂ"			:"ʂǂ"	,
	r"[sš]!"			:"ʃ!"	,
	r"[sšł]ǁ"			:"ɬǁ"	,
#	Pulmonics unaffected
	"ṭ"					:"ʈ"    ,
	"tł"				:"L"	,
	"ʼ"					:"ʔ"	,
	"ṇ"					:"ɳ"	,
	"n"					:"n̪"	,
	"ň"					:"ɲ"	,
	"č"					:"C"	,
	"ts"				:"D"	,
	"tṣ"				:"ʈ͡ʂ"	,
	"t"					:"D"	,
	"j"					:"ɟ"	,
#	Fix ejective, dental affricate
	"E"					:"ʼ"	,
	"D"					:"t͡s̪"	,
	"C"					:"t͡ʃ"	,
	"L"					:"t͡ɬ"	,
# 	Vowel segment unrolling
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
#	Monophthongize
	r"([aeiɔu])\1"		:r"\1ː"	,
#	Bring nasal in
	"ːN"				:"Nː"	,
#	Pre-nasal click nasality
	r"([aeiɔu])ᵑ"		:r"\1Nᵑ",
#	Creaky-Nasal fix
	r"C([aeiɔu]N)"		:r"\1̰",
#	Nasalize
	"aN"				:"ã"	,
	"eN"				:"ẽ"	,
	"ɔN"				:"ɔ̃"	,
	"iN"				:"ĩ"	,
	"uN"				:"ũ"	,
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

def log(s):
	with open("pronunciatorlog.txt",'a',encoding="utf-8") as f:
		f.write(s+"\n")

def pronunciate(text, debug=False):
	text = superLowerCase(text)

	for patt in IPAsubs:
		repl = IPAsubs[patt]


		text = re.sub(patt,repl,text)

		if debug:
			log(text)

	return text


pronunciate("Ʇila ǃxaje nǁotṣo ǂòõ.",debug=True)