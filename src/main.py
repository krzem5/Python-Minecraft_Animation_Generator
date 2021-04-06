import clipboard
import random



INIT_CMD="summon falling_block ~ ~1 ~ {Time:1,BlockState:{Name:\"minecraft:redstone_block\"},Passengers:[{id:armor_stand,Health:0,Passengers:[{id:\"minecraft:falling_block\",Time:1,BlockState:{Name:\"minecraft:activator_rail\"},Passengers:[%s{id:\"minecraft:command_block_minecart\",Command:\"setblock ~ ~-2 ~ air\"},{id:\"minecraft:command_block_minecart\",Command:\"setblock ~ ~-2 ~ command_block[facing=up]\"},{id:\"minecraft:command_block_minecart\",Command:\"setblock ~ ~1 ~ command_block{auto:1,Command:\\\"fill ~ ~ ~ ~ ~-2 ~ air\\\"}\"},{id:\"minecraft:command_block_minecart\",Command:\"kill @e[type=command_block_minecart,distance=..1]\"}]}]}]}"
INIT_CMD_LAST="summon falling_block ~ ~1 ~ {Time:1,BlockState:{Name:\"minecraft:redstone_block\"},Passengers:[{id:armor_stand,Health:0,Passengers:[{id:\"minecraft:falling_block\",Time:1,BlockState:{Name:\"minecraft:activator_rail\"},Passengers:[%s{id:\"minecraft:command_block_minecart\",Command:\"setblock ~ ~1 ~ command_block{auto:1,Command:\\\"fill ~ ~ ~ ~ ~-3 ~ air\\\"}\"},{id:\"minecraft:command_block_minecart\",Command:\"kill @e[type=command_block_minecart,distance=..1]\"}]}]}]}"
CMD="{id:\"minecraft:command_block_minecart\",Command:\"%s\"},"
ID_CHARS="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
ID_LEN=16
CMD_X_OFF=2
MAX_CMD_LEN=32500
BLOCK_OFF=0.0000001



def generate(pdt):
	def _rand_id(x=ID_LEN):
		return "".join([ID_CHARS[random.randint(0,len(ID_CHARS)-1)] for _ in range(0,x)])
	def _next(x,xa,y,z,za,d):
		x+=xa
		if (xa==1 and x==sz-1):
			d=("south" if za==1 else "north")
		elif (xa==1 and x==sz):
			d="west"
			xa=-1
			x=sz-1
			z+=za
		elif (xa==-1 and x==0):
			d=("south" if za==1 else "north")
		elif (xa==-1 and x==-1):
			d="east"
			xa=1
			x=0
			z+=za
		if (za==1 and z==sz-1 and ((xa==1 and x==sz-1) or (xa==-1 and x==0))):
			d="up"
		elif (za==1 and z==sz):
			z=sz-1
			za=-1
			y+=1
			x=min(max(x,0),sz-1)
		elif (za==-1 and z==0 and ((xa==1 and x==sz-1) or (xa==-1 and x==0))):
			d="up"
		elif (za==-1 and z==-1):
			z=0
			za=1
			y+=1
			x=min(max(x,0),sz-1)
		return [x,xa,y,z,za,d]
	_sp_id=_rand_id()
	_rm_id=_rand_id()
	_tr_id=_rand_id()
	_bl_id=_rand_id()
	spl=[]
	ol=[]
	td={}
	pd={}
	for p in pdt["paths"].keys():
		pd[p]=_rand_id(ID_LEN-6)
		ol+=[f"scoreboard players add @e[type=armor_stand,tag=_bl_{_bl_id},scores={{_path_{pd[p]}=0..}}] _path_{pd[p]} 1"]
		t=0
		for k in pdt["paths"][p]:
			k["x"]=(k["x"] if "x" in k.keys() else 0)
			k["y"]=(k["y"] if "y" in k.keys() else 0)
			k["z"]=(k["z"] if "z" in k.keys() else 0)
			ol+=[f"execute as @e[type=armor_stand,tag=_bl_{_bl_id},scores={{_path_{pd[p]}={int(t)}..{int(t+k['t']*20)}}}] at @s run tp @s ~{k['x']/(k['t']*20)} ~{k['y']/(k['t']*20)} ~{k['z']/(k['t']*20)}"]
			t+=k['t']*20
		ol+=[f"scoreboard players set @e[type=armor_stand,tag=_bl_{_bl_id},scores={{_path_{pd[p]}={int(t)}..}}] _path_{pd[p]} -1"]
	for bt in pdt["blocks"].keys():
		for b in pdt["blocks"][bt]:
			for p in b["paths"]:
				if (p["trigger"] not in td.keys()):
					td[p["trigger"]]=_rand_id()
			id_=_rand_id()
			spl+=[f"execute at @e[tag=_bl_spw_{_sp_id}] run fill ~{b['pos']['x']} ~{b['pos']['y']} ~{b['pos']['z']} ~{b['pos']['x']} ~{b['pos']['y']-1} ~{b['pos']['x']} air",f"execute at @e[tag=_bl_spw_{_sp_id}] run summon minecraft:armor_stand ~{b['pos']['x']} ~{b['pos']['y']-BLOCK_OFF*b['pos']['y']} ~{b['pos']['z']} {{Invulnerable:1b,Small:1b,Marker:1b,Invisible:1b,NoBasePlate:1b,PersistenceRequired:1b,NoGravity:1b,DisabledSlots:4144959,Tags:[\"_spw\",\"_b_{id_}\",\"_bl_{_bl_id}\"],Passengers:[{{id:\"minecraft:falling_block\",Tags:[\"_b_{id_}\",\"_bl_{_bl_id}\"],Time:1,BlockState:{{Name:\"minecraft:{bt}\"}}}},{{id:\"minecraft:shulker\",NoAI:1b,Silent:1b,Invulnerable:1b,PresistenceRequired:1b,DeathLootTable:\"\",ActiveEffects:[{{Id:14,Amplifier:255,Duration:1000000,Ambient:1,ShowParticles:0b}}],Tags:[\"_b_{id_}\",\"_bl_{_bl_id}\"]}}]}}"]+[f"scoreboard players set @e[type=armor_stand,tag=_b_{id_},tag=_spw] _path_{pd[p['path']]} -1" for p in b["paths"]]+[f"execute as @e[tag=_bl_tr_{_tr_id},tag=_bl_tr_{td[p['trigger']]}] run scoreboard players set @e[type=armor_stand,tag=_b_{id_},scores={{_path_{pd[p['path']]}=-1}}] _path_{pd[p['path']]} 0" for p in b["paths"]]
	ol=[f"execute as @e[type=falling_block,tag=_bl_{_bl_id}] run data merge entity @s {{Time:1,FallDistance:0}}",f"execute at @e[type=armor_stand,tag=_bl_{_bl_id},tag=!_bl_spw_{_sp_id},tag=!_bl_rm_{_rm_id},tag=!_bl_tr_{_tr_id}] run fill ~ ~ ~ ~ ~-1 ~ air"]+spl+[f"kill @e[tag=_bl_spw_{_sp_id}]",f"tag @e[type=armor_stand,tag=_bl_{_bl_id},tag=_spw] remove _spw"]+ol+[f"execute at @e[tag=_bl_rm_{_rm_id}] run tp @e[tag=_bl_{_bl_id},distance=..5] ~ -100 ~",f"kill @e[tag=_bl_rm_{_rm_id}]",f"kill @e[tag=_bl_{_bl_id},tag=_bl_tr_{_tr_id}]",f"give @a[tag=_give_{_sp_id}] minecraft:armor_stand{{display:{{Name:\"{{\\\"text\\\":\\\"Spawn Blocks\\\",\\\"italic\\\":false}}\",Lore:[\"{{\\\"text\\\":\\\"Place this down to spawn\\\",\\\"color\\\":\\\"white\\\",\\\"italic\\\":false}}\",\"{{\\\"text\\\":\\\"the structure\\\",\\\"color\\\":\\\"purple\\\",\\\"bold\\\":true,\\\"italic\\\":false}}\"]}},EntityTag:{{NoGravity:1b,Invulnerable:1b,Small:1b,Marker:1b,Invisible:1b,NoBasePlate:1b,PersistenceRequired:1b,Tags:[\"_bl_{_bl_id}\",\"_bl_spw_{_sp_id}\"],DisabledSlots:4144959}}}} 1",f"give @a[tag=_give_{_sp_id}] minecraft:armor_stand{{display:{{Name:\"{{\\\"text\\\":\\\"Remove Blocks\\\",\\\"italic\\\":false}}\",Lore:[\"{{\\\"text\\\":\\\"Place this down to remove\\\",\\\"color\\\":\\\"white\\\",\\\"italic\\\":false}}\",\"{{\\\"text\\\":\\\"the nearest structure\\\",\\\"color\\\":\\\"purple\\\",\\\"bold\\\":true,\\\"italic\\\":false}}\"]}},EntityTag:{{NoGravity:1b,Invulnerable:1b,Small:1b,Marker:1b,Invisible:1b,NoBasePlate:1b,PersistenceRequired:1b,Tags:[\"_bl_{_bl_id}\",\"_bl_rm_{_rm_id}\"],DisabledSlots:4144959}}}} 1"]+[f"give @a[tag=_give_{_sp_id}] minecraft:armor_stand{{display:{{Name:\"[{{\\\"text\\\":\\\"Trigger \\\",\\\"italic\\\":false,\\\"color\\\":\\\"white\\\"}},{{\\\"text\\\":\\\"{tn}\\\",\\\"color\\\":\\\"purple\\\",\\\"bold\\\":true,\\\"italic\\\":false}}]\",Lore:[\"{{\\\"text\\\":\\\"Place this down to active\\\",\\\"color\\\":\\\"white\\\",\\\"italic\\\":false}}\",\"[{{\\\"text\\\":\\\"trigger \\\",\\\"color\\\":\\\"white\\\",\\\"italic\\\":false}},{{\\\"text\\\":\\\"{tn}\\\",\\\"color\\\":\\\"purple\\\",\\\"bold\\\":true,\\\"italic\\\":false}}]\"]}},EntityTag:{{NoGravity:1b,Invulnerable:1b,Small:1b,Marker:1b,Invisible:1b,NoBasePlate:1b,PersistenceRequired:1b,Tags:[\"_bl_{_bl_id}\",\"_bl_tr_{_tr_id}\",\"_bl_tr_{td[tn]}\"],DisabledSlots:4144959}}}} 1" for tn in td.keys()]+[f"tag @a remove _give_{_sp_id}"]
	x=0
	xa=1
	y=0
	z=0
	za=1
	d="east"
	t="repeating"
	l=len(ol)+len(pd.keys())+3
	sz=round(l**(1/3)*10**5)/10**5
	if (int(sz)**3!=l):
		sz=int(sz)+1
	else:
		sz=int(sz)
	bol=[]
	for i,k in enumerate(ol):
		k=k.replace("\\","\\\\").replace("\"","\\\"")
		bol+=[f"setblock ~{x+CMD_X_OFF} ~{y-2} ~{z} {t}_command_block[facing={d}]{{auto:1b,Command:\"{k}\"}}"]
		t="chain"
		x,xa,y,z,za,d=_next(x,xa,y,z,za,d)
	bol=[f"scoreboard objectives add _path_{pd[p]} dummy" for p in pd.keys()]+[f"fill ~{x+CMD_X_OFF} ~-2 ~ ~{x+CMD_X_OFF+sz-1} ~{sz-3} ~{sz-1} air",f"fill ~{CMD_X_OFF-1} ~-2 ~ ~{CMD_X_OFF-1} ~-2 ~1 air",f"setblock ~{CMD_X_OFF-1} ~-2 ~ dark_oak_wall_sign[facing=west]{{Text1:\"{{\\\"text\\\":\\\"===============\\\",\\\"clickEvent\\\":{{\\\"action\\\":\\\"run_command\\\",\\\"value\\\":\\\"tag @p add _give_{_sp_id}\\\"}},\\\"bold\\\":true,\\\"color\\\":\\\"gray\\\"}}\",Text2:\"{{\\\"text\\\":\\\"Give\\\",\\\"color\\\":\\\"blue\\\"}}\",Text3:\"{{\\\"text\\\":\\\"Armor Stands\\\",\\\"bold\\\":true,\\\"color\\\":\\\"dark_green\\\"}}\",Text4:\"{{\\\"text\\\":\\\"===============\\\",\\\"bold\\\":true,\\\"color\\\":\\\"gray\\\"}}\"}}",f"setblock ~{CMD_X_OFF-1} ~-2 ~1 dark_oak_wall_sign[facing=west]{{Text1:\"{{\\\"text\\\":\\\"===============\\\",\\\"clickEvent\\\":{{\\\"action\\\":\\\"run_command\\\",\\\"value\\\":\\\"data merge block ~{x+1} ~{y} ~{z-1} {{auto:1b}}\\\"}},\\\"bold\\\":true,\\\"color\\\":\\\"gray\\\"}}\",Text2:\"{{\\\"text\\\":\\\"Remove\\\",\\\"color\\\":\\\"blue\\\"}}\",Text3:\"{{\\\"text\\\":\\\"Structure\\\",\\\"bold\\\":true,\\\"color\\\":\\\"dark_red\\\"}}\",Text4:\"{{\\\"text\\\":\\\"===============\\\",\\\"bold\\\":true,\\\"color\\\":\\\"gray\\\"}}\"}}"]+bol
	t=""
	a=[x+0,xa+0,y+0,z+0,za+0,d+""]
	for _ in range(0,len(pd.keys())):
		a=_next(*a)
	nxa,_,nya,nza,_,_=_next(*a)
	nxb,_,nyb,nzb,_,_=_next(*_next(*a))
	for i,k in enumerate([f"scoreboard objectives remove _path_{pd[p]}" for p in pd.keys()]+[f"kill @e[tag=_bl_{_bl_id}]",f"fill ~{-nxa-1} ~{-nya} ~{-nza} ~{-nxa-1} ~{-nya} ~{-nza+1} air",f"fill ~{-nxb} ~{-nyb} ~{-nzb} ~{-nxb+sz} ~{-nyb+sz} ~{-nzb+sz} air"]):
		k=k.replace("\\","\\\\").replace("\"","\\\"")
		bol+=[f"setblock ~{x+CMD_X_OFF} ~{y-2} ~{z} {t}command_block[facing={d}]{{auto:{('0' if len(t)==0 else '1')}b,Command:\"{k}\"}}"]
		t="chain_"
		x,xa,y,z,za,d=_next(x,xa,y,z,za,d)
	o=[""]
	for k in bol:
		k=k.replace("\\","\\\\").replace("\"","\\\"")
		if (len(o[-1])+len(CMD%(k))+len(INIT_CMD)>=MAX_CMD_LEN):
			o+=[""]
		o[-1]+=CMD%(k)
	return [(INIT_CMD if i<len(o)-1 else INIT_CMD_LAST)%(o[i]).replace("~0 ","~ ") for i in range(0,len(o))]



o=generate({
	"paths": {
		"down": [
			{
				"y": -3,
				"t": 2
			}
		],
		"up": [
			{
				"y": 3,
				"t": 2
			}
		]
	},
	"blocks": {
		"dark_oak_planks": [
			{
				"pos": {
					"x": 0,
					"y": 0,
					"z": 0
				},
				"paths": [
					{
						"trigger": "DOWN",
						"path": "down"
					},
					{
						"trigger": "UP",
						"path": "up"
					}
				]
			},
			{
				"pos": {
					"x": 0,
					"y": 1,
					"z": 0
				},
				"paths": [
					{
						"trigger": "DOWN",
						"path": "down"
					},
					{
						"trigger": "UP",
						"path": "up"
					}
				]
			},
			{
				"pos": {
					"x": 0,
					"y": 2,
					"z": 0
				},
				"paths": [
					{
						"trigger": "DOWN",
						"path": "down"
					},
					{
						"trigger": "UP",
						"path": "up"
					}
				]
			}
		]
	}
})
if (len(o)==1):
	clipboard.copy(o[0])
with open("./out.txt","w") as f:
	f.write("\n\n\n".join(o))
