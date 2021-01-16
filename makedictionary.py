import pronunciator
from texescape import escape as esc

fname = "dictionary/dictionary.lift"

grammatical_abbreviation = {
	"Personal pronoun":"pers.\\-pr.",
	"Pronoun":"pron.",
	"Noun":"n.",
	"Verb":"v.",
	"Intransitive verb":"v.\\-intr.",
	"Transitive verb":"v.\\-tr.",
	"Adjective":"adj.",
	"Noun classifier":"clf.",
	"Cardinal numeral":"card.\\-num.",
	"Ordinal numeral":"ord.\\-num.",
	"Postposition":"post.",
	"Preverb":"preverb",
	"Adverb":"adv.",
	"Reflexive pronoun":"refl.\\-pr.",
	"Coordinating connective":"conj.",
	"Relative pronoun":"rel.\\-pr."
}


import xml.etree.ElementTree as ET

import re
bwc_pattern = re.compile(r"(ʘ|ǃ|ǂ|ǁ|qʼ|x)[eièì]")

root = ET.parse(fname).getroot()


refs = {}


texstrings = []


class Entry():
	def __init__(self,local):
		self.local = local
		self.senses = []

		self.ipa = pronunciator.pronunciate(local)

		self.TestConstraints()

	def TestConstraints(self):
		bwc = bwc_pattern.match(self.local)
		if(bwc):
			errorstr = "ERROR: entry %s violates bwc"%(self.local)
			with open('makediclog.txt','a',encoding='utf-8') as f:
				f.write(errorstr+"\n")
			print(errorstr.encode("ascii","ignore"))

	def Format(self):
		sensesstring = "\\dictsensesep".join(map(lambda x:x.Format(), self.senses))

		return '\\dictentry{%s}{%s}{%s}'%(self.local,self.ipa,sensesstring)

	def FormatRef(self):
		return "\\dictref{%s}"%self.local

class Sense():
	def __init__(self,parent):
		self.examples = []
		self.clfs = []
		self.parent = parent


	def Format(self):
		if(len(self.clfs)>0):
			clf_string = "\\dictclassifiers{%s}"%(",".join(map(lambda ref:refs[ref].parent.FormatRef(),self.clfs)))
		else:
			clf_string = ""
		examples_string = " ".join(map(lambda x:x.Format(), self.examples))
		extras = examples_string + clf_string
		return "\\dictsense{%s}{%s}{%s}"%(self.gramm,self.definition,extras)

class Example():
	def __init__(self, local, translation):
		self.local = local
		self.translation = translation

	def Format(self):
		return "\\dictexample{%s}{%s}"%(self.local,self.translation)

lexicon = []

for entrytag in root.findall('entry'):

	# create entry

	lex = entrytag.find('lexical-unit')

	local = lex.find('form/text').text

	entry = Entry(local)


	for sensetag in entrytag.findall('sense'):
		# make sense

		sense = Sense(entry)


		# extract grammatical info (part of speech)

		grammtag = sensetag.find('grammatical-info')

		gramm = "N/A" if grammtag is None else grammtag.attrib['value']

		if gramm in grammatical_abbreviation:
			gramm = grammatical_abbreviation[gramm]

		sense.gramm = gramm

		# extract definition (use default gloss if definition empty)

		gloss = esc(sensetag.find('gloss/text').text.replace("CLF_","").replace("_"," "))

		defintag = sensetag.find('definition')
		definition = gloss
		if defintag:
			definitiontext = defintag.find("form/text").text
			if not definitiontext is None:
				definition = esc(definitiontext)

		sense.definition = definition
		
		# populate examples

		examplestrings = []
		for exampletag in sensetag.findall('example'):
			try:
				exampletext,exampletransl = (exampletag.find('form/text').text, esc(exampletag.find('translation/form/text').text))
			except AttributeError:
				continue
			sense.examples.append(Example(exampletext,exampletransl))

		# populate clf definitions

		for clftag in sensetag.findall('relation[@type="Classifier"]'):
			sense.clfs.append(clftag.attrib['ref'])
		
		# setup reference

		refs[sensetag.attrib['id']] = sense


		# append sense to entry
		entry.senses.append(sense)

	# append entry to lexicon
	lexicon.append(entry)
	

# sort time
 
sorting_alphabet = "ʇʘǃǂǁʼaãàbčdeẽèiĩìjklłmnṇňŋoõòpqrsšṣtṭuũùx"


def sortingKey(entry):
	word = entry.local

	output = []
	for c in word:
		try:
			output.append(sorting_alphabet.index(c))
		except ValueError:
			output.append(len(sorting_alphabet))
	return output


lexicon.sort(key=sortingKey)

texout = "\n".join(map(lambda x:x.Format(),lexicon))



with open("book/dictionary.tex","w",encoding='utf-8') as f:
	f.write(texout)
