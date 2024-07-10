from datetime import datetime
import json
from os.path import basename, isfile
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds
import py3Dmol
import re

def progress_bar(total, current)->None:
  """
  Description
  -----------
    Display a progress bar indicating the completion status of a task.

  Parameters
  ----------
    - total (int): The total number of units representing the task's completion.
    - current (int): The current progress, representing the number of units completed.

  Example
  -------
  >>> progress_bar(100, 50)
  Processing . . .
    50.0%  |===========>                |  50 / 100
  """
  percent = round(current/total * 100, 2)
  num_progress_bar = round(int(percent) // 5)
  num_redidual_bar =  20 - num_progress_bar
  progress_bar_string = "\033[34mProcessing . . .  \n  {}%  |{}>{}|  {} / {}\033[0m".format(percent, num_progress_bar * "=", num_redidual_bar * " ", current, total)
  print(progress_bar_string)

def is_ipython():
  try:
    __IPYTHON__
    return True
  except NameError:
    return False

def husl_palette(pal_len:int)->list:
  """
  Description
  -----------
  seaborn husl palette without seaborn 

  Parameters
  ----------
    - pal_len(int) : n_colors in husl palette ( 2 =< pal_len =< 9 )

  Returns
  -------
    - palette(list) : RGB list
  """
  match pal_len:
    case 2:
      return [(0.9677975592919913, 0.44127456009157356, 0.5358103155058701),
              (0.21044753832183283, 0.6773105080456748, 0.6433941168468681)]
    case 3:
      return [(0.9677975592919913, 0.44127456009157356, 0.5358103155058701),
              (0.3126890019504329, 0.6928754610296064, 0.1923704830330379),
              (0.23299120924703914, 0.639586552066035, 0.9260706093977744)]
    case 4:
      return  [(0.9677975592919913, 0.44127456009157356, 0.5358103155058701),
               (0.5920891529639701, 0.6418467016378244, 0.1935069134991043),
               (0.21044753832183283, 0.6773105080456748, 0.6433941168468681),
               (0.6423044349219739, 0.5497680051256467, 0.9582651433656727)]
    case 5:
      return  [(0.9677975592919913, 0.44127456009157356, 0.5358103155058701),
               (0.6804189127793346, 0.6151497514677574, 0.19405452111445337),
               (0.20125317221201128, 0.6907920815379025, 0.47966761189275336),
               (0.2197995660828324, 0.6625157876850336, 0.7732093159317209),
               (0.8004936186423958, 0.47703363533737203, 0.9579547196007522)]
    case 6:
      return  [(0.9677975592919913, 0.44127456009157356, 0.5358103155058701),
               (0.7350228985632719, 0.5952719904750953, 0.1944419133847522),
               (0.3126890019504329, 0.6928754610296064, 0.1923704830330379),
               (0.21044753832183283, 0.6773105080456748, 0.6433941168468681),
               (0.23299120924703914, 0.639586552066035, 0.9260706093977744),
               (0.9082572436765556, 0.40195790729656516, 0.9576909250290225)]
    case 7:
      return  [(0.9677975592919913, 0.44127456009157356, 0.5358103155058701),
               (0.7757319041862729, 0.5784925270759935, 0.19475566538551875),
               (0.5105309046900421, 0.6614299289084904, 0.1930849118538962),
               (0.20433460114757862, 0.6863857739476534, 0.5407103379425205),
               (0.21662978923073606, 0.6676586160122123, 0.7318695594345369),
               (0.5049017849530067, 0.5909119231215284, 0.9584657252128558),
               (0.9587050080494409, 0.3662259565791742, 0.9231469575614251)]
    case 8:
      return  [(0.9677975592919913, 0.44127456009157356, 0.5358103155058701),
               (0.8087954113106306, 0.5634700050056693, 0.19502642696727285),
               (0.5920891529639701, 0.6418467016378244, 0.1935069134991043),
               (0.19783576093349015, 0.6955516966063037, 0.3995301037444499),
               (0.21044753832183283, 0.6773105080456748, 0.6433941168468681),
               (0.22335772267769388, 0.6565792317435265, 0.8171355503265633),
               (0.6423044349219739, 0.5497680051256467, 0.9582651433656727),
               (0.9603888539940703, 0.3814317878772117, 0.8683117650835491)]
    case 9:
      return  [(0.9677975592919913, 0.44127456009157356, 0.5358103155058701),
               (0.8369430560927636, 0.5495828952802333, 0.1952683223448124),
               (0.6430915736746491, 0.6271955086583126, 0.19381135329796756),
               (0.3126890019504329, 0.6928754610296064, 0.1923704830330379),
               (0.20582072623426667, 0.6842209016721069, 0.5675558225732941),
               (0.2151139535594307, 0.6700707833028816, 0.7112365203426209),
               (0.23299120924703914, 0.639586552066035, 0.9260706093977744),
               (0.731751635642941, 0.5128186367840487, 0.9581005178234921),
               (0.9614880299080136, 0.3909885385134758, 0.8298287106954371)]
    case _:
      raise ValueError(f"{pal_len} is not in [2, 9], 2 =< pal_len =< 9")

def markers_(lens:int)->list:
  """
  Description
  -----------
  matplotlib markers

  Parameters
  ----------
    - len(lens) : number of plots ( 2 =< lens =< 9 )

  Returns
  -------
    - palette(list) : RGB list
  """
  match lens:
    case 2:
      return ["v", "^"]
    case 3:
      return ["2", "3", "4"]
    case 4:
      return [">", "<", "^", "v"]
    case 5:
      return [">", "<", "^", "s", "D"]
    case 6:
      return ["1", "3", "4", "v", "<", ">"]
    case 7:
      return ["1", "3", "4", "v", "<", ">", "^"]
    case 8:
      return ["1", "2", "3", "4", "v", "<", ">", "^"]
    case 9:
      return [">", "<", "^", "s", "D", "1", "2", "3", "4"]
    case _:
      raise ValueError(f"{lens} is not in [2, 9], 2 =< lens =< 9")


def json_dump(trajDIASresult:dict, trajFile:str, resultSavePath:str="./aimDIAS_result.json", title=None, note=None)->None:
  """
  Description
  -----------
  Dump the aimDIAS results into a JSON file.

  Parameters
  ----------
    - trajDIASresult (dict): The aimDIAS results to be dumped.
    - trajFile (str): The path to the trajectory file.
    - resultSavePath (str, optional): The path to save the JSON file. Default is "./aimDIAS_result.json".
    - title (str, optional): Title for the JSON file. Default is None.
    - note (str, optional): Additional note for the JSON file. Default is None.
  """
  with open(resultSavePath, "w") as file:
    json.dump({
      "title"           : title if title else "",
      "note"            : note if note else "",
      "trajectory_file" : basename(trajFile) if isfile(trajFile) else "",
      "submission_date" : str(datetime.now().strftime("%Y-%m-%d %H:%M")),
      "result"          : trajDIASresult
        }, file, indent=4, ensure_ascii=False)
    

def draw_xyz(trajFile:str, charge:int=0, idx:int=0)->py3Dmol.view:
  """
  Description
  -----------
  Visualize the molecule with atomic indice using py3Dmol.

  Parameters
  ----------
    - trajFile (str) : The trajectory file path or trajectory format string to read.
    - charge (int) : The charge of the whole system.
    - idx (int) : IRC index in trajectory file. Idx starts with 0

  Returns
  -------
    - viewer(py3Dmol.view) : The py3Dmol viewer object.
  """
  # load idx - xyz string
  if isfile(trajFile):
    with open(trajFile, "r") as file:
      traj = file.read()
  else:
    traj = trajFile

  # Split the trajectory file into multiple XYZ format strings
  pattern = re.compile("(\s?\d+\n.*\n(\s*[a-zA-Z]{1,2}(\s+-?\d+.\d+){3,3}\n?)+)")
  matched = pattern.findall(traj)

  molecule_string = tuple(map(lambda groups : groups[0], matched))[idx]

  # convert xyz string to mol block
  raw_mol = Chem.MolFromXYZBlock(molecule_string)
  rdDetermineBonds.DetermineBonds(raw_mol,charge=charge) # bond determine
  block_mol = Chem.MolToMolBlock(raw_mol)

  # py3Dmol viewer
  p = py3Dmol.view(width=550,height=550)
  p.removeAllModels()
  p.addModel(block_mol,'sdf')
  p.setStyle({'stick':{}})
  p.setBackgroundColor('0xeeeeee')

  # add index label
  for atom in raw_mol.GetAtoms():
      idx = atom.GetIdx()
      symbol = atom.GetSymbol()
      pos = raw_mol.GetConformer().GetAtomPosition(idx)
      x, y, z = pos.x, pos.y, pos.z
      label_text = '{:>2}'.format(idx + 1)
      p.addLabel(label_text, {'position': {'x': x, 'y': y, 'z': z}, 'fontSize': 14, 'backgroundColor':"black","fontColor":"white"})
  p.zoomTo()
  return p.show()


