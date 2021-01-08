import pronunciator
from texescape import escape as esc

fname = "dictionary/dictionary.lift"

grammatical_abbreviation = {
	"Personal pronoun":"pers.pr.",
	"Pronoun":"pron.",
	"Noun":"n.",
	"Verb":"v.",
	"Intransitive verb":"v.intr.",
	"Transitive verb":"v.tr.",
	"Adjective":"adj.",
	"Noun classifier":"clf.",
	"Cardinal numeral":"card.num.",
	"Ordinal numeral":"ord.num.",
	"Postposition":"post.",
	"Preverb":"preverb",
	"Adverb":"adv.",
	"Reflexive pronoun":"refl.pr.",
	"Coordinating connective":"conj.",
	"Relative pronoun":"rel.pr."
}


import xml.etree.ElementTree as ET

root = ET.parse(fname).getroot()



texstrings = []

for entry in root.findall('entry'):
	lex = entry.find('lexical-unit')

	local = lex.find('form/text').text




	senses = []

	

	for sensetag in entry.findall('sense'):
		grammtag = sensetag.find('grammatical-info')

		gramm = "N/A" if grammtag is None else grammtag.attrib['value']

		if gramm in grammatical_abbreviation:
			gramm = grammatical_abbreviation[gramm]

		gloss = esc(sensetag.find('gloss/text').text.replace("CLF_","").replace("_"," "))

		defintag = sensetag.find('definition')
		definition = gloss
		if defintag:
			definitiontext = defintag.find("form/text").text
			if not definitiontext is None:
				definition = esc(definitiontext)

		
		
		examplestrings = []
		for exampletag in sensetag.findall('example'):
			try:
				example = (exampletag.find('form/text').text, esc(exampletag.find('translation/form/text').text))
			except AttributeError:
				continue
			examplestring = "\\dictexample{%s}{%s}"%example
			examplestrings.append(examplestring)

		senses.append((gramm,definition," ".join(examplestrings)))

	


	sensesstring = "\\dictsensesep".join(["\\dictsense{%s}{%s}{%s}"%sense for sense in senses])

	ipa = pronunciator.pronunciate(local)
	
	texstring = '\\dictentry{%s}{%s}{%s}'%(local,ipa,sensesstring)



	#import sys
	#sys.stdout.buffer.write((texstring+"\n").encode('utf-8'))

	texstrings.append(texstring)

# sort time
 
sorting_alphabet = "ʇǃǂǁʼaãàbčdeẽèiĩìjklłmnṇňŋoõòpqrsšṣtṭuũùx"


def sortingKey(word):
	output = []
	for c in word:
		try:
			output.append(sorting_alphabet.index(c))
		except ValueError:
			output.append(len(sorting_alphabet))
	return output


texstrings.sort(key=sortingKey)

texout = "\n".join(texstrings)
#texout = texstrings[0]
#print(texstrings[0])

with open("book/dictionary.tex","w",encoding='utf-8') as f:
	f.write(texout)
