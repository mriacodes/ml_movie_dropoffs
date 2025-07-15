# Movie Viewing Behavior Analysis Project

## 📁 Data Files Overview

This project contains multiple CSV files at different stages of processing. Below is a guide to understand what each file contains and when to use them.

---

## 🗂️ File Descriptions

### **Raw Data Files**
- **`dropoffs.csv`** - Original survey responses (unprocessed)
- **`responses_partially_cleaned.csv`** - Initial cleaning applied
- **`imdb_data.csv`** - Movie metadata from IMDB for synthetic data generation

### **Synthetic Data Files**
- **`dropoffs_with_movies_simple.csv`** - Survey responses enhanced with synthetic movie data
  - Contains 5 finished movies and 5 unfinished movies per respondent
  - Includes reasons for dropping movies

### **Processed Data Files (MAIN OUTPUTS)**

#### 📋 **For Human Analysis & Reporting**
**`responses_cleaned_human_readable.csv`**
- **Purpose**: Visual inspection, presentations, exploratory analysis
- **Content**: Original survey responses with cleaned formatting
- **Features**:
  - Segregated genre preferences (e.g., "Action, Comedy, Drama")
  - Segregated drop reasons (e.g., "Boring Plot, Too Long")
  - Engagement levels (Low, Medium, High)
  - All demographic information in readable format

#### 🤖 **For Machine Learning**
**`responses_discretized_for_ml.csv`**
- **Purpose**: Training machine learning algorithms
- **Content**: All features converted to numerical format
- **Features**:
  - 30+ ML-ready features
  - Binary encoded preferences (0/1)
  - Discretized categorical variables
  - Target variables for prediction

#### 📊 **Complete Reference**
**`responses_complete_processed.csv`**
- **Purpose**: Complete dataset with all original and processed features
- **Content**: Both raw responses AND processed features
- **Use**: Reference when you need to trace back from processed features to original responses

---

## 🎯 **Which File Should You Use?**

### For **Data Exploration & Visualization**
✅ Use: `responses_cleaned_readable.csv`
- Easy to read and understand
- Perfect for creating charts and graphs
- Good for stakeholder presentations

### For **Machine Learning Model Building**
✅ Use: `responses_discretized_for_ml.csv`
- Ready for algorithms (Decision Trees, Neural Networks, etc.)
- All features are numerical
- Contains target variables for prediction

### For **Data Validation & Debugging**
✅ Use: `responses_complete_processed.csv`
- Contains everything (original + processed)
- Good for checking preprocessing logic
- Useful for troubleshooting

---

## 🎯 Target Variables (For ML Models)

The ML dataset contains these prediction targets:

1. **`high_engagement_user`** (0/1) - Predicts highly engaged users
2. **`high_dropout_user`** (0/1) - Predicts users likely to drop movies

---

## 🔧 Feature Categories

### **Demographic Features** (Discretized)
- Age group (1-6)
- Gender (1-5) 
- Education level (1-6)
- Movie watching frequency (1-5)

### **Preference Features** (Binary 0/1)
- Genre preferences (12 genres)
- Completion behaviors
- Dropout patterns

### **Behavioral Features** (Binary 0/1)
- Drop reasons (6 categories)
- Viewing habits
- Engagement patterns

### **Aggregate Features** (Numerical)
- Total liked genres
- Total drop reasons
- Engagement score
- Dropout tendency

---

## 🚀 Quick Start Guide

### **For Data Analysts**
```python
# Load human-readable data
import pandas as pd
df = pd.read_csv('responses_cleaned_human_readable.csv')

# Explore genre preferences
print(df['Segregated_Genre_Preferences'].value_counts())

# Analyze engagement levels
print(df['Engagement_Level'].value_counts())
```

### **For Machine Learning Engineers**
```python
# Load ML-ready data
import pandas as pd
df = pd.read_csv('responses_discretized_for_ml.csv')

# Separate features and targets
feature_cols = [col for col in df.columns if col not in ['Respondent_ID', 'high_engagement_user', 'high_dropout_user']]
X = df[feature_cols]
y = df['high_engagement_user']  # or 'high_dropout_user'

# Ready for model training!
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
```

---

## 📊 Checkbox Response Handling

**Important**: Checkbox questions (e.g., "Select all that apply") have been separated into individual binary features.

**Original**: `"Boring plot, Too long, Technical issues"`
**Becomes**:
- `drops_due_to_boring_plot`: 1
- `drops_due_to_too_long`: 1  
- `drops_due_to_technical_issues`: 1
- `drops_due_to_poor_acting`: 0
- etc.

This allows for:
- Quantitative analysis of each reason
- Machine learning compatibility
- Statistical correlation analysis

---

## 🎯 Recommended Algorithms

Based on the data structure, these algorithms are recommended:

1. **Decision Tree Based Methods** - Good interpretability
2. **Neural Networks** - Complex pattern recognition
3. **Naive Bayes Classifier** - Works well with categorical features
4. **Nearest Neighbor Classification** - Good for recommendation systems

---

## 📋 Data Quality Notes

- **No missing values** in ML features (filled with 0)
- **77 total respondents**
- **Balanced target variables** (~50/50 split)
- **Mixed feature types**: Binary, categorical, continuous
- **Memory usage**: ~0.15 MB per file

---

## 🔍 File Metadata

Additional information is stored in:
- **`feature_info.json`** - Complete feature lists, mappings, and metadata

---

## ❓ Need Help?

- For **data exploration**: Start with `responses_cleaned_human_readable.csv`
- For **model building**: Use `responses_discretized_for_ml.csv`
- For **debugging**: Check `responses_complete_processed.csv`
- For **feature details**: Refer to `feature_info.json`

---

## 📈 Project Status

✅ Data collection complete
✅ Data preprocessing complete
✅ Feature engineering complete
🔄 **NEXT**: Model building and evaluation
🔄 **READY FOR**: Algorithm experimentation

---

*Last updated: July 9, 2025*
*Team: Movie Completion Prediction Project*
