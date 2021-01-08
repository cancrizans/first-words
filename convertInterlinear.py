import sys
import xml.etree.ElementTree as ET
text = ET.parse(sys.argv[1]).getroot()[0]



phrases = []


for paragraph in text.iter('paragraph'):
	
	phrases += paragraph[0].findall('phrase')


def redditParsePhrase(phrase):
	words = phrase.find('words').findall('word')
	N = len(words)
	output = "|"*(N+1)+"\n"

	output += "|:-"*N+"|\n"

	original_words = []
	gloss_words = []
	for w in words:
		punct  = w.find(".item/[@type='punct']")
		if not (punct is None):
			original_words.append(punct.text)
			gloss_words.append("")
		else:
			try:
				original_words.append(w.find("./item[@type='txt']").text)
				gloss_words.append(w.find("./item[@type='gls']").text)
			except AttributeError:
				print("Err",w.tag,w.attrib)


	#for w in words:
	#	print(w.tag,w.attrib)
	#original_words = [w.find("./item[@type='txt']").text for w in words]

	#print(original_words)

	output += "|" + "|".join(map(lambda ow : "**"+ow+"**" ,original_words)) + "|\n"

	#gloss_words = [w.find("./item[@type='gls']").text for w in words]

	#print(gloss_words)

	output += "|" + "|".join(map(lambda gw : gw ,gloss_words)) + "|\n"

	output += "*" +  phrase.find("./item[@type='gls']").text.strip() + "*"

	return output


redditput = "\n\n".join(map(redditParsePhrase,phrases))

with open('output.md','w',encoding="utf-8") as f:
	f.write(redditput)