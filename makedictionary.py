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


entryrefs = {}
refs = {}


texstrings = []


class Entry():
	def __init__(self,local,entryid):
		self.local = local
		self.senses = []

		self.ipa = pronunciator.pronunciate(local)

		self.variantOf = None
		self.id = entryid

		entryrefs[self.id] = self

		self.TestConstraints()

	def TestConstraints(self):
		bwc = bwc_pattern.match(self.local)
		if(bwc):
			errorstr = "ERROR: entry %s violates bwc"%(self.local)
			with open('makediclog.txt','a',encoding='utf-8') as f:
				f.write(errorstr+"\n")
			print(errorstr.encode("ascii","ignore"))

	def Format(self):
		if self.variantOf:
			contentstring = "\\dictvariantof{%s}"%entryrefs[self.variantOf].FormatRef()
		else:
			contentstring = "\\dictsensesep".join(map(lambda x:x.Format(), self.senses))

		return '\\dictentry{%s}{%s}{%s}'%(self.local,self.ipa,contentstring)

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
	entryid = entrytag.attrib['id']

	entry = Entry(local,entryid)



	# determine if variant

	
	for relationtag in entrytag.findall("relation"):

		traittag = relationtag.find("trait[@name='variant-type']")

		if not (traittag is None):
			entry.variantOf = relationtag.attrib['ref']


	for sensetag in entrytag.findall('sense'):
		if entry.variantOf:
			break

		# make sense

		sense = Sense(entry)


		# extract grammatical info (part of speech)

		grammtag = sensetag.find('grammatical-info')

		gramm = "N/A" if grammtag is None else grammtag.attrib['value']

		if gramm in grammatical_abbreviation:
			gramm = grammatical_abbreviation[gramm]

		sense.gramm = gramm

		# extract definition (use default gloss if definition empty)
		glosstag = sensetag.find('gloss/text')
		if glosstag is None:
			#print(ET.tostring(entrytag,encoding='utf-8'))
			#print(ET.tostring(sensetag,encoding='utf-8'))
			#raise ValueError
			gloss = ""
		else:
			gloss = esc(glosstag.text.replace("CLF_","").replace("_"," "))

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
 
sorting_alphabet = "ʇʘǃǂǁʼaãàbčdeẽèiĩìjklłmnṇñŋoõòpqrsšṣtṭuũùx"

click_regex = re.compile(r"[ʘʇǃǂǁ]")

def rank_consonant(c):

	click_match = click_regex.search(c)
	if click_match:
		leading = 0
		click = click_match.group(0)

		before,after = click_regex.split(c,maxsplit=1)

		return [0, click, before, after]


	else:
		#not a click
		return [10,c]



vowel_regex = re.compile(r"[aeiouàèìòù]")



keyed_lexicon = {}

for entry in lexicon:
	consonants = vowel_regex.split(entry.local,maxsplit=2)
	if len(consonants)>1:
		consonant = consonants[1] if consonants[0] == "" else consonants[0]
	else:
		raise ValueError

	if not (consonant in keyed_lexicon):
		keyed_lexicon[consonant] = []
	keyed_lexicon[consonant].append(entry)


for consonant in keyed_lexicon:
	keyed_lexicon[consonant].sort(key = lambda entry : entry.local)




def formatLetterSec(letter):
	return "\\lettersection{%s}"%letter + \
		"\n".join(map(lambda x:x.Format(),keyed_lexicon[letter]))

sortedkeys =  list(keyed_lexicon.keys())
sortedkeys.sort(key = rank_consonant)




texout = "\n".join(map(formatLetterSec,sortedkeys))

with open("book/dictionary.tex","w",encoding='utf-8') as f:
	f.write(texout)
