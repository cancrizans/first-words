import os

sources = [
"nwats",
"suntongue_and_the_night"
]


import convertInterlinear as ci


for s in sources:
	path = os.path.join("glosses",s+".flextext")
	inter = ci.FormatInterlinear(path,mode="tex")
	with open(os.path.join("book/interlinears" , s+".tex"),'w', encoding='utf-8') as f:
		f.write(inter)


