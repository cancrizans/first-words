import xml.etree.ElementTree as ET
import argparse


import pronunciator

from texescape import escape as esc



def FormatInterlinear(filename,mode="reddit"):

	text = ET.parse(filename).getroot()[0]


	class InterlinearParsingException:
		pass

	if not (mode in ["reddit","tex","beamer"]):
		raise InterlinearParsingException("Error: unrecognized mode.")

	phrases = []


	for paragraph in text.iter('paragraph'):
		
		phrases += paragraph[0].findall('phrase')



	if mode == "reddit":
		blank_gloss = "" 
	elif mode in ["tex","beamer"]:
		blank_gloss = "{}"

	def FormatPhrase(phrase):


		words = phrase.find('words').findall('word')
		N = len(words)

		if(mode == "reddit"):
			output = "|"*(N+1)+"\n"
			output += "|:-"*N+"|\n"
		elif (mode =="beamer"):
			output = "\\interlinearslide{" 
		elif (mode == "tex"):
			output = "\\begin{exe}\n \\ex \n"

		original_words = []
		gloss_words = []

		original_run = ""

		for w in words:
			punct  = w.find(".item/[@type='punct']")
			if not (punct is None):
				original_words.append(punct.text)
				gloss_words.append(blank_gloss)

				original_run += punct.text
			else:

				isclf = False
				morphemes =  w.find("./morphemes")
				if morphemes:
					for morpheme in morphemes.findall("./morph"):
						msa = morpheme.find("./item[@type='msa']")
						if not msa is None:
							
							if msa.text.strip() == 'nclf':
								
								isclf = True



				try:
					original_word = w.find("./item[@type='txt']").text
					if mode in ["tex","beamer"]:
						original_word = "{"+esc(original_word)+"}"
					original_words.append(original_word)

					gloss_word = w.find("./item[@type='gls']").text

					if mode == "reddit" and isclf:
						gloss_word = "CLF^(%s)"%gloss_word
					if mode in ["tex","beamer"]:
						gloss_word = esc(gloss_word)
						if isclf:
							gloss_word = "\\CLF{%s}"%gloss_word
						else:
							gloss_word = gloss_word.replace(" ",".")

					

					gloss_words.append(gloss_word)

					original_run += " "+ original_word
				except AttributeError:
					print("Err",w.tag,w.attrib)


		translation = phrase.find("./item[@type='gls']").text.strip()

		if mode == "reddit":
			output += "|" + "|".join(map(lambda ow : "**"+ow+"**" ,original_words)) + "|\n"



			output += "|" + "|".join(map(lambda gw : gw ,gloss_words)) + "|\n"

			output += "*" +  translation + "*"
		elif mode == "beamer":
			output += original_run.strip() + "}{"
#			output += esc(pronunciator.pronunciate(original_run)) + "}{"
			output +=  " ".join(map(lambda gw : gw ,gloss_words)) + "}{"
			output += esc(translation) + "}"
		elif mode == "tex":
			output += "\\gll " + " ".join(original_words) + "\\\\ \n"
			output += " ".join(map(lambda gw : gw ,gloss_words)) + "\\\\ \n"
			output += "\\glt " + translation + "\n"
			output += "\\end{exe}"


		return output


	formatOutput = "\n\n".join(map(FormatPhrase,phrases))
	return formatOutput



if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("file")
	parser.add_argument("--mode", default="reddit")
	parser.add_argument("--output", default="output.md")
	args = parser.parse_args()


	input_text_filename = args.file
	with open(args.output,'w',encoding="utf-8") as f:
		f.write(FormatInterlinear(input_text_filename,args.mode))