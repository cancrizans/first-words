# -*- coding: UTF-8 -*-
import sys

print(sys.stdout.encoding)


# vowels_back = ["a", "o", u"ɔ"]

# vowels = ["a", "e", "i", "o", u"ɔ"]

# click_articulations = [u"|", u"!", u"ǂ", u"ǁ"]

# click_nasal = "ᵑ"

# click_glottalized = "ˀ"

# click_frication = u"\u0361χ"

# click_pre = {
# 	u"|" : [u"s̪"],
# 	u"!" : ["s","r"],
# 	u"ǂ" : [u"ʃ"],
# 	u"ǁ" : [u"ɬ"]
# }


# pulmonics = ["p", "c", "k", "m", "l", u"ɲ", u"ɬ", "r", u"s̪", "s", u"ʃ"]


vowels_back = ["a", "o", u"ò"]

vowels = ["a", "e", "i", "o", u"ò"]

click_articulations = [u"c", u"q", u"g", u"x"]

click_nasal = "n"

click_glottalized = "'"

click_frication = "h"

click_pre = {
	u"c" : ["þ"],
	u"q" : ["s","r","š","ɬ"],
	u"g" : ["š","r"],
	u"x" : ["ɬ"]
}


pulmonics = ["p", "j", "k", "m", "l", "ñ", "ɬ", "r", "þ", "s", "š"]



import random

def random_vowel():
	return random.choice(vowels)

def random_vowel_back():
	return random.choice(vowels_back)


def random_click():

	articulation = random.choice(click_articulations)

	nasal = (random.random()<0.6)
	glottalized = (random.random()<0.6) if nasal else False

	frication = (not glottalized) and (random.random()<0.5)

	pre = ""
	if(not nasal):
		if(random.random()<0.3):
			pre = random.choice(click_pre[articulation])

	click = (click_nasal if nasal else pre) + articulation + (click_frication if frication else "") + (click_glottalized if glottalized else "")

	return (click, articulation)

def random_pulmonic():
	return (random.choice(pulmonics),"P")

def random_leading_consonant():
	if(random.random()<0.3):
		return random_pulmonic()
	else:
		return random_click()



def random_word():
	second_syllable = random.random() < 0.7
	prevowel = random.random() < 0.2

	word = ""

	if prevowel:
		word += random_vowel()

	cons = random_leading_consonant()

	if(cons[1] in ("q", "g")):
		vowel = random_vowel_back()
	else:
		vowel = random_vowel()

	word += cons[0] + vowel

	if(second_syllable):
		word += random_pulmonic()[0] + random_vowel()

	return word

words = [random_word() for i in range(200)]

f = open("output.txt","w",encoding='utf-8')
f.write("\n".join(words))
f.close()
