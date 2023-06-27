from classes.json_module import JSONModule

json_module = JSONModule('../data/variables.json')

vim = json_module.get('vim')
nivel220 = json_module.get('nivel220')

intercept = json_module.get('linregress_CV_VIM_intercept')

difference = abs(nivel220 - vim)

intercept += difference

json_module.set('linregress_CV_VIM_intercept', intercept)
