import pandas as pd
from impedance.models.circuits import CustomCircuit

def getRaw(x):
    return complex(x["Re"],x["Im"])

def getReal(x):
    return x.real

def getImag(x):
    return x.imag

def fitData(rawDF,circuit,initial):

    circuit = circuit.replace("Q","CPE")

    df=rawDF.copy()

    freq = df["f"]
    freq = freq.to_numpy()
    df["raw"] = df.apply(getRaw,axis=1)
    Z = df["raw"].to_numpy()


    initial_guess = initial
    circuit = CustomCircuit(circuit, initial_guess=initial_guess)

    circuit.fit(freq,Z)

    print(circuit.parameters_)

    freqList = df["f"].to_numpy()
    fit = circuit.predict(freqList)

    model = pd.Series(fit)

    df["model"] = model

    df["mRe"] = df["model"].apply(getReal)
    df["mIm"] = -df["model"].apply(getImag)


    df = df.drop(["raw"],axis=1)
    df = df.drop(["model"],axis=1)

    outDF = pd.DataFrame()
    outDF["f"] = df["f"]
    outDF["mRe"] = df["mRe"]
    outDF["mIm"] = df["mIm"]


    return outDF,circuit.parameters_









