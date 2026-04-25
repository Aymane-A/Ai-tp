import pandas as pd

import numpy as np

from fpdf import FPDF

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import Perceptron
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns


def generate_hospital_data(n: int) -> pd.DataFrame:
    """

    generate synthetic hospital data with probabilistic distribution


    parameters:

        n (int) : number of data points (patients)


    returns:

        pd.DataFrame : dataFrame with synthetic hospital data

    """


    np.random.seed(42)  # pour la reproductibilité


    # 1. Unique patient ID

    patient_id = np.arange(1, n + 1)

    # 2. Sex Bernoulli(0.5) => 0 (Female), 1 (Male)

    sex = np.random.binomial(1, 0.5, size=n)

    # 3. Age: Uniform(20, 80)

    age = np.random.uniform(20, 80, size=n).round(1)

    # 4. Severrity: Multinomial([0.5, 0.3, 0.2]) mapped to ['low', 'medium', 'high']

    severity_probs = [0.5, 0.3, 0.2]

    severity_levels = ["low", "medium", "high"]

    severity_indices = np.random.choice(len(severity_levels), size=n, p=severity_probs)

    severity = [severity_levels[i] for i in severity_indices]


    # 5. Blood Pressure: Normal(120, 15)

    blood_pressure = np.random.normal(loc=120, scale=15, size=n).round(1)

    # 6. Readmissions: Poisson(lambda = 2)

    readmissions = np.random.poisson(lam=2, size=n)


    # Create DataFrame

    df = pd.DataFrame(

        {

            "patient_id": patient_id,

            "sex": sex,

            "age": age,

            "severity": severity,

            "blood_pressure": blood_pressure,

            "readmissions": readmissions,

        }
    )

    return df



def visualize_hospital_data(df: pd.DataFrame):
    """

    VISUALIZE HOSPITAL DATA WITH HISTOGRAMS AND BAR PLOTS


    PAREMETERS:

        df(pd.DataFrame) : dataFrame CONTAINING HOSPITAL DATA
    """


    sns.set(style="whitegrid")  # noqa: F821

    fig, axes = plt.subplots(3, 2, figsize=(14, 12))  # noqa: F821
    axes = axes.flatten()


    # 1. Sex (Bar Plot)

    sns.countplot(x="sex", data=df, ax=axes[0], hue="sex", palette="Set2", legend=False)  # noqa: F821

    axes[0].set_title("Sex distribution (0=Female, 1=Male)")


    # 2. Age (Histogram)

    sns.histplot(df["age"], bins=20, kde=True, ax=axes[1], color="skyblue")  # noqa: F821

    axes[1].axvline(

        df["age"].mean(),
        color="red",

        linestyle="--",

        label=f"Mean: {df['age'].mean():.2f}",
    )

    axes[1].legend()

    axes[1].set_title("Age distribution")


    # 3. Severity (Bar Plot)

    sns.countplot(x="severity", data=df, ax=axes[2], hue="severity", palette="pastel")  # noqa: F821

    axes[2].set_title("Severity Levels")


    # 4. Blood Pressure (Histogram)

    sns.histplot(df["blood_pressure"], bins=20, kde=True, ax=axes[3], color="Orange")  # noqa: F821

    axes[3].axvline(

        df["blood_pressure"].mean(),
        color="red",

        linestyle="--",

        label=f"Mean: {df['blood_pressure'].mean():.2f}",
    )

    axes[3].legend()

    axes[3].set_title("Blood Pressure distribution")


    # 5. Readmissions (Histogram)

    sns.histplot(df["readmissions"], bins=10, kde=False, ax=axes[4], color="lightgreen")  # noqa: F821

    axes[4].axvline(

        df["readmissions"].mean(),
        color="red",

        linestyle="--",

        label=f"Mean: {df['readmissions'].mean():.2f}",
    )

    axes[4].legend()

    axes[4].set_title("Readmissions distribution")


    # Empty 6th plot

    fig.delaxes(axes[5])


    plt.tight_layout()  # noqa: F821

    plt.show()  # noqa: F821



def save_hospital_data(df: pd.DataFrame, format: str, filename: str):
    """

    SAVE HOSPITAL DATA IN VARIOUS FORMATS


    PARAMETERS:

       df(pd.DataFrame): THE DATAFRAME TO SAVE

       format (str): FORMAT TO SAVE IN: CSV, EXCEL, JSON, XML, PDF

       filename(str): NAME OF THE FILE (WITHOUT EXTENSION)
    """

    format = format.lower()

    supported_formats = ["csv", "excel", "json", "xml", "pdf"]


    if format not in supported_formats:

        raise ValueError(

            f"Format '{format}' not supportted. choose from {supported_formats}."
        )


    if format == "csv":

        df.to_csv(f"{filename}.csv", index=False)

    elif format == "excel":

        df.to_excel(f"{filename}.xlsx", index=False)

    elif format == "json":

        df.to_json(f"{filename}.json", orient="records", indent=4)

    elif format == "xml":

        df.to_xml(f"{filename}.xml", index=False)

    elif format == "pdf":

        pdf = FPDF()

        pdf.add_page()

        pdf.set_font("Arial", size=10)

        col_width = pdf.w / (len(df.columns) + 1)

        row_height = 10

        spacing = 1


        # HEADER

        for col in df.columns:

            pdf.cell(col_width, row_height * spacing, str(col), border=1)

        pdf.ln(row_height * spacing)


        # Data rows (limit to first 30 for readability)

        for _, row in df.head(30).iterrows():

            for item in row:

                pdf.cell(col_width, row_height * spacing, str(item), border=1)

            pdf.ln(row_height * spacing)


        pdf.output(f"{filename}.pdf")




## data preparation function 

def prepare_data_for_classification(df, target_col):
    """

    prepare data for ML classification:

    - Label encode categorical features

    - Scale numerical features

    - split into training (60%), validation (20%), test (20%) 


    parameters:

        df : pandas dataFrame

        target_col : column to be predicted


    returns:

        x_train, x_val, x_test, y_train, y_val, y_test : Label_encoders
    """


    # Encode categorical variables

    df_encoded = df.copy()
    label_encoders = {}
    for col in df.select_dtypes(include=['object']).columns:
        le=LabelEncoder()
        df_encoded[col]=le.fit_transform(df[col])
        label_encoders[col]=le

    # Separate features and target

    X = df_encoded.drop(columns=[target_col, "patient_id"]) # exclude ID

    y = df_encoded[target_col]


    # Standard scaling (important for KNN, MLP)

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)
    

    # Split into training (60%), and temp (40%)

    X_train, X_temp, y_train, y_temp = train_test_split(

        X_scaled, y, test_size=0.4, random_state=42)


    #then split temp into validation (20%) and test (20%)

    X_val, X_test, y_val, y_test = train_test_split(

        X_temp, y_temp, test_size=0.5, random_state=42)
    

    return X_train, X_val, X_test, y_train, y_val, y_test, label_encoders


def train_and_evaluate_models(X_train, X_val, y_train, y_val):
    models = {
        "KNN": KNeighborsClassifier(n_neighbors=3),
        "Perceptron": Perceptron(max_iter=1000),
        "NaiveBayes": GaussianNB(),
        "NeuralNet": MLPClassifier(hidden_layer_sizes=(50,), max_iter=1000)

    }

    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_val)
        report = classification_report(y_val, y_pred, output_dict=True)
        conf_mat = confusion_matrix(y_val, y_pred)
        results[name] = {
            'model': model,
            'report': report,
            'confusion_matrix': conf_mat
        }
    return results

## confusion matrix

def plot_confusion_heatmaps(results, class_names):
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    for i, (name, result) in enumerate(results.items()):
        sns.heatmap(result['confusion_matrix'], annot=True, fmt="d", cmap="Blues", ax=axes[i], xticklabels=class_names, yticklabels=class_names)
        axes[i].set_title(f"{name} Confusion Matrix")
        axes[i].set_xlabel("Predicted")
        axes[i].set_ylabel("Actual")
        
    plt.tight_layout()
    plt.show()


def plot_kiviat(results, metric='f1-score'):
    """
    Create a radar chart for a chosen across models and classes
    """

    labels = ['high', 'medium', 'low']
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]  

    fig = plt.figure(figsize=(8, 6)) 
    ax = plt.subplot(111, polar=True)

    for model_name, result in results.items():
        stats = [result['report'][str(i)][metric] for i in range(3)]
        stats += stats[:1]
        ax.plot(angles, stats, label=model_name)
        ax.fill(angles, stats, alpha=0.2)
        

    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    plt.title(f"Radar Plot: {metric}")
    plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1)) 
    plt.show()


#Generate a small simple for trying 

sample_data = generate_hospital_data(10)
sample_data

#visualize the sample data
visualize_hospital_data(sample_data)

#try saving sample data as PDF and CSV
save_hospital_data(sample_data, 'CSV', "sample_hospital_data")
save_hospital_data(sample_data, 'PDF', "sample_hospital_data")
save_hospital_data(sample_data, 'EXCEL', "sample_hospital_data")
save_hospital_data(sample_data, 'JSON', "sample_hospital_data")
save_hospital_data(sample_data, 'XML', "sample_hospital_data")       


df = generate_hospital_data(300)
x_train, x_val, x_test, y_train, y_val, y_test, encoders = prepare_data_for_classification(df, target_col="severity")
results = train_and_evaluate_models(x_train, x_val, y_train, y_val)
plot_confusion_heatmaps(results, class_names=['low','medium','high'])
plot_kiviat(results, metric='f1-score')

