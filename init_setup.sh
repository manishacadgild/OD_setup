echo [$(date)]: "START" 
export __VERSION__=3.9
echo [$(date)]: "creating env with python  ${__VERSION__}" 
conda create --prefix ./env python=${__VERSION__} -y
echo [$(date)]: "activating the environment" 
source activate ./env
echo [$(date)]: "install requirements" 
pip install -r requirements.txt
echo [$(date)]: "initialize the git setup"
git init
echo [$(date)]: "END"