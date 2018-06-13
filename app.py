# import libraries
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, render_template, redirect, jsonify


#################################################
# Database Setup
#################################################


#engine = create_engine("sqlite:///hawaii.sqlite",connect_args={'check_same_thread':False})
engine = create_engine("sqlite:///belly_button_biodiversity.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)


# Save reference to the table
OTU = Base.classes.otu
Samples = Base.classes.samples
Samples_Metadata = Base.classes.samples_metadata

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
# create instance of Flask app
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# route that renders index.html template and finds Mars info from MongoDB
@app.route("/")
def home():
    """Return the dashboard homepage."""
    return render_template("index.html")

@app.route('/names')
def samples():
    """Returns a list of sample names"""
    results = session.query(Samples_Metadata.SAMPLEID).all()
	
    sample_names = []
    
    for sample in results:
        sample_name = "BB_" + str(sample)
        sample_name = sample_name.replace("(","")
        sample_name = sample_name.replace(",)","")
        sample_names.append(sample_name)

    return jsonify(sample_names)


@app.route('/otu')
def otu():
    """List of OTU descriptions."""
    results = session.query(OTU.lowest_taxonomic_unit_found).all()

    otu_desc = []

    for desc in results:
        desc = str(desc).replace("(","").replace(",)","").replace("'","")
        otu_desc.append(str(desc))


    return jsonify(otu_desc)

@app.route('/metadata/<sample>')
def meta(sample):
    """Returns a json dictionary of sample metadata"""
    sample = str(sample).replace("BB_","")
    age = str(session.query(Samples_Metadata.AGE).filter(Samples_Metadata.SAMPLEID == sample).all())
    bbtype = str(session.query(Samples_Metadata.BBTYPE).filter(Samples_Metadata.SAMPLEID == sample).all()).replace("[('","").replace("',)]","")
    ethnicity = str(session.query(Samples_Metadata.ETHNICITY).filter(Samples_Metadata.SAMPLEID == sample).all()).replace("[('","").replace("',)]","")
    gender = str(session.query(Samples_Metadata.GENDER).filter(Samples_Metadata.SAMPLEID == sample).all()).replace("[('","").replace("',)]","")
    location = str(session.query(Samples_Metadata.LOCATION).filter(Samples_Metadata.SAMPLEID == sample).all()).replace("[('","").replace("',)]","")
    sample = int(sample)
    age = int((age.replace("[(","")).replace(",)]",""))

    meta_dict = {'AGE':age, 'BBTYPE':bbtype, "ETHNICITY":ethnicity, "GENDER":gender, "LOCATION":location, "SAMPLEID":sample}

    return jsonify(meta_dict)


@app.route('/wfreq/<sample>')
def wwf(sample):
    """Returns an integer value for the weekly washing frequency `WFREQ`"""
    sample = str(sample).replace("BB_","")
    wfreq = str(session.query(Samples_Metadata.WFREQ).filter(Samples_Metadata.SAMPLEID == sample).all()).replace("[('","").replace("',)]","")
    wfreq = int((wfreq.replace("[(","")).replace(",)]",""))

    return jsonify(wfreq)

@app.route('/samples/<sample>')
def smpl(sample):
    """Return a list of dictionaries containing sorted lists  for `otu_ids`"""
    results = session.query(Samples.otu_id, getattr(Samples, sample)).order_by(getattr(Samples, sample).desc()).all()
    
    df = pd.DataFrame(results, columns=['otu_ids', 'sample_values'])
    
    otu_dict = {
            "otu_ids": df["otu_ids"].values.tolist(),
            "sample_values": df["sample_values"].values.tolist()
    }
    otu_list = []
    otu_list.append(otu_dict)
    return jsonify(otu_list)


	
if __name__ == "__main__":
    app.run(debug=True)
