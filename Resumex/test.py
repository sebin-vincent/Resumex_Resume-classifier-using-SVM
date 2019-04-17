import pandas
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer

#from svm import count_vect

from sklearn.externals import joblib


filename='final_svm model.sav'

loaded_model = joblib.load(open(filename, 'rb'))


#following 'software_engineer is variable of string which is resume for testing

# resume='''b'Call Center Operator Resume\nSydney Holcomb\n123 Main Street, San Francisco, CA 94122\nHome: 000-000-0000 | Cell: 000-000-0000\nemail@example.com\nProfessional Summary\nFriendly and eloquent Call Center Operator looking for a position to use skills for the best customer service\npossible.Long-term commitment with a strong desire and ability to advance within the company.\nCore Qualifications\n\xef\x82\xb7 Excellent customer service even to difficult callers\n\xef\x82\xb7 Problem solving skills necessary to keep customers and clients satisfied\n\xef\x82\xb7 Multitasking skills to continue speaking to a customer while searching for information\n\xef\x82\xb7 Ability to remain calm in stressful situations\n\xef\x82\xb7 Desire to learn more that can be applied to the job\n\xef\x82\xb7 Strong work ethic leading to efficient and complete service\n\xef\x82\xb7 Great sales experience and persuasion techniques\n\xef\x82\xb7 Ability to work a telephone switchboard\n\xef\x82\xb7 Familiar with multiple computer programs and systems with a capacity to learn others\nExperience\nCall Center Operator\n11/1/2007 - Present\nMasters & Co.\nLester, MA\n\n\xef\x82\xb7\n\xef\x82\xb7\n\xef\x82\xb7\n\xef\x82\xb7\n\nAnswer phones and customer requests and complaints in an efficient manner\nTransfer calls to appropriate place\nReport to supervisor with any problems or suggestions to better work atmosphere\nAssist customers in a timely manner to avoid long waiting times\n\xef\x82\xb7 Calm frustrated or upset customers by providing excellent and friendly service\n\nCall Center Operator\n8/1/2004 - 11/1/2007\nMilford Inc.\nWyatt, MA\n\n\xef\x82\xb7 Placed phone calls offering customers high quality products and services\n\xef\x82\xb7 Answered all customer questions and complaints in a professional manner\n\xef\x82\xb7 Strived to meet a daily sales goal as an individual and a team\n\nEducation\n\n\x0cHigh School Diploma\nXXXX - XXXX\nWyatt High School\nWyatt, MA'"
# '''

count_vect=joblib.load('vect.joblib','rb')

def predict(resume):
    return (loaded_model.predict(count_vect.transform([resume])))