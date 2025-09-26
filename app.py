import os
import yaml

from linkml.generators.pydanticgen import PydanticGenerator

import streamlit as st
import streamlit_pydantic as sp

st.set_page_config(page_title='Bilayers Schema Creation')

model_yaml = '../bilayers/tests/test_config/validate_schema.yaml' 

with open(model_yaml,'r') as fd:
    model = yaml.safe_load(fd)

if "linkml" not in model["prefixes"].keys():
    model["prefixes"]["linkml"]="https://w3id.org/linkml/"

with open('bilayers_model_raw.py','w') as f:
    f.write(PydanticGenerator(yaml.dump(model),extra_fields="allow",metadata_mode='full').serialize())

#hacks
with open('bilayers_model.py','w') as fw:
    with open('bilayers_model_raw.py','r') as f:
        for line in f.readlines():
            line = line.replace('list[SubTypeEnum]','set[SubTypeEnum]')
            line = line.replace('default: Any','default: str')
            line = line.replace('label: Any','label: str')
            line = line.replace(' value: Optional[Any]',' value: Optional[str]')
            line = line.replace('range: Any','range: str')
            fw.write(line)

os.remove('bilayers_model_raw.py')

from bilayers_model import SpecContainer
data = sp.pydantic_input(key="spec_container",model=SpecContainer, group_optional_fields="expander" )
st.download_button("Download your config file here",yaml.dump({k:v for k,v in data.items() if 'spec_container' not in k}),'config.yaml')