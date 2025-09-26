import os
import yaml
import urllib

from linkml.generators.pydanticgen import PydanticGenerator

import streamlit as st
import streamlit_pydantic as sp

st.set_page_config(page_title='Bilayers Schema Creation')

st.write("# Bilayers schema configuration")

st.session_state["created_pydantic"]=os.path.exists('bilayers_model.py')

if not st.session_state["created_pydantic"]:

    web_model_yaml = 'https://raw.githubusercontent.com/bilayer-containers/bilayers/refs/heads/main/tests/test_config/validate_schema.yaml' 
    local_model_yaml = 'config.yaml'

    urllib.request.urlretrieve(web_model_yaml,local_model_yaml)

    with open(local_model_yaml,'r') as fd:
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

    os.remove(local_model_yaml)
    os.remove('bilayers_model_raw.py')

    st.session_state["created_pydantic"]=True

from bilayers_model import SpecContainer
data = sp.pydantic_input(key="spec_container",model=SpecContainer, group_optional_fields="expander" )
st.download_button("Download your config file here",yaml.dump({k:v for k,v in data.items() if 'spec_container' not in k}),'config.yaml')