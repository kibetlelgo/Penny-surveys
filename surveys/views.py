from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CustomUserRegistrationForm
from .models import UserProfile
from django.views.decorators.http import require_POST
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
import random

# Create your views here.

def get_survey_data(survey_title):
    """Get survey data for instructions page"""
    # Survey data from the surveys list
    surveys_data = {
        'SurveysPlus': {'reward': 160, 'estimated_time': 11, 'questions': 7},
        'Safaricom M-PESA': {'reward': 210, 'estimated_time': 15, 'questions': 15},
        'Equity Bank': {'reward': 140, 'estimated_time': 12, 'questions': 10},
        'Naivas Supermarket': {'reward': 120, 'estimated_time': 12, 'questions': 10},
        'Kenya Airways': {'reward': 260, 'estimated_time': 15, 'questions': 13},
        'Brookside Dairy': {'reward': 100, 'estimated_time': 12, 'questions': 15},
        'Jumia Kenya': {'reward': 180, 'estimated_time': 12, 'questions': 10},
        'KCB Bank': {'reward': 170, 'estimated_time': 12, 'questions': 10},
        'Twiga Foods': {'reward': 130, 'estimated_time': 9, 'questions': 6},
        'Co-operative Bank': {'reward': 110, 'estimated_time': 8, 'questions': 9},
        'Zuku': {'reward': 190, 'estimated_time': 11, 'questions': 7},
        'Kipepeo Clothing': {'reward': 125, 'estimated_time': 9, 'questions': 6},
        'KPLC': {'reward': 150, 'estimated_time': 9, 'questions': 11},
        'Bidco Africa': {'reward': 115, 'estimated_time': 8, 'questions': 12},
        'Safaricom Home Fibre': {'reward': 220, 'estimated_time': 11, 'questions': 10},
        'Artcaffe': {'reward': 145, 'estimated_time': 10, 'questions': 12},
    }
    
    # Return survey data or default values
    return surveys_data.get(survey_title, {'reward': 100, 'estimated_time': 10, 'questions': 5})

def generate_survey_questions(survey_title):
    """Generate random questions based on survey title"""
    
    # Question templates for different survey types
    question_templates = {
        'Safaricom M-PESA': [
            {
                'question': 'How long have you been using M-PESA?',
                'type': 'multiple_choice',
                'options': ['Less than 1 year', '1-3 years', '3-5 years', '5-10 years', 'More than 10 years'],
                'required': True
            },
            {
                'question': 'What is your primary use of M-PESA?',
                'type': 'multiple_choice',
                'options': ['Sending money to family', 'Receiving payments', 'Buying airtime/data', 'Paying bills (electricity, water)', 'Shopping online', 'Saving money', 'Business transactions'],
                'required': True
            },
            {
                'question': 'How often do you use M-PESA in a typical week?',
                'type': 'multiple_choice',
                'options': ['1-2 times', '3-5 times', '6-10 times', '11-20 times', 'More than 20 times'],
                'required': True
            },
            {
                'question': 'How satisfied are you with M-PESA\'s transaction speed?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'How satisfied are you with M-PESA\'s customer service?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'What is your average transaction amount on M-PESA?',
                'type': 'multiple_choice',
                'options': ['Less than Ksh 100', 'Ksh 100 - 500', 'Ksh 500 - 1,000', 'Ksh 1,000 - 5,000', 'Ksh 5,000 - 10,000', 'More than Ksh 10,000'],
                'required': True
            },
            {
                'question': 'Have you ever experienced any issues with M-PESA transactions?',
                'type': 'yes_no',
                'required': True
            },
            {
                'question': 'If yes, what type of issues have you encountered?',
                'type': 'multiple_choice',
                'options': ['Failed transactions', 'Delayed money transfers', 'Network connectivity issues', 'Agent unavailability', 'High transaction fees', 'Security concerns', 'None'],
                'required': False
            },
            {
                'question': 'How important is M-PESA to your daily financial activities?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'What new features would you like to see in M-PESA?',
                'type': 'text',
                'required': False
            },
            {
                'question': 'Do you use M-PESA for business purposes?',
                'type': 'yes_no',
                'required': True
            },
            {
                'question': 'What is your age group?',
                'type': 'multiple_choice',
                'options': ['18-25', '26-35', '36-45', '46-55', '55+'],
                'required': True
            },
            {
                'question': 'What is your occupation?',
                'type': 'multiple_choice',
                'options': ['Student', 'Employee', 'Business owner', 'Self-employed', 'Farmer', 'Retired', 'Other'],
                'required': True
            },
            {
                'question': 'How do you primarily access M-PESA?',
                'type': 'multiple_choice',
                'options': ['USSD (*234#)', 'M-PESA App', 'Safaricom App', 'Agent services', 'Bank integration'],
                'required': True
            },
            {
                'question': 'Would you recommend M-PESA to others?',
                'type': 'yes_no',
                'required': True
            }
        ],
        'Equity Bank': [
            {
                'question': 'How long have you been a customer of Equity Bank?',
                'type': 'multiple_choice',
                'options': ['Less than 1 year', '1-3 years', '3-5 years', '5-10 years', 'More than 10 years'],
                'required': True
            },
            {
                'question': 'Which Equity Bank services do you use most frequently?',
                'type': 'multiple_choice',
                'options': ['Savings account', 'Current account', 'Loans', 'Mobile banking', 'Investment products', 'Credit cards', 'Insurance'],
                'required': True
            },
            {
                'question': 'How satisfied are you with Equity Bank\'s overall service?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'How would you rate Equity Bank\'s customer service?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'How satisfied are you with Equity Bank\'s mobile banking app?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'What improvements would you suggest for Equity Bank\'s mobile app?',
                'type': 'text',
                'required': False
            },
            {
                'question': 'How often do you visit an Equity Bank branch?',
                'type': 'multiple_choice',
                'options': ['Daily', 'Weekly', 'Monthly', 'Quarterly', 'Rarely'],
                'required': True
            },
            {
                'question': 'How much do you typically transact through Equity Bank per month?',
                'type': 'multiple_choice',
                'options': ['Less than Ksh 10,000', 'Ksh 10,000 - 50,000', 'Ksh 50,000 - 100,000', 'Ksh 100,000 - 500,000', 'More than Ksh 500,000'],
                'required': True
            },
            {
                'question': 'What is your occupation?',
                'type': 'multiple_choice',
                'options': ['Student', 'Employee', 'Business owner', 'Self-employed', 'Retired', 'Other'],
                'required': True
            },
            {
                'question': 'Would you recommend Equity Bank to others?',
                'type': 'yes_no',
                'required': True
            }
        ],
        'Naivas Supermarket': [
            {
                'question': 'How often do you shop at Naivas Supermarket?',
                'type': 'multiple_choice',
                'options': ['Daily', 'Weekly', 'Bi-weekly', 'Monthly', 'Rarely'],
                'required': True
            },
            {
                'question': 'What products do you usually buy from Naivas?',
                'type': 'multiple_choice',
                'options': ['Groceries', 'Household items', 'Fresh produce', 'Beverages', 'Personal care', 'All of the above'],
                'required': True
            },
            {
                'question': 'How would you rate Naivas\' product quality?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'How satisfied are you with Naivas\' customer service?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'What factors influence your choice of supermarket?',
                'type': 'text',
                'required': False
            },
            {
                'question': 'How much do you typically spend per shopping trip?',
                'type': 'multiple_choice',
                'options': ['Less than Ksh 500', 'Ksh 500 - 1,000', 'Ksh 1,000 - 2,000', 'Ksh 2,000 - 5,000', 'More than Ksh 5,000'],
                'required': True
            },
            {
                'question': 'Do you use Naivas\' loyalty program?',
                'type': 'yes_no',
                'required': True
            },
            {
                'question': 'How would you rate Naivas\' store cleanliness and organization?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'What improvements would you suggest for Naivas?',
                'type': 'text',
                'required': False
            },
            {
                'question': 'Would you recommend Naivas Supermarket to others?',
                'type': 'yes_no',
                'required': True
            }
        ],
        'Kenya Airways': [
            {
                'question': 'How often do you travel by air?',
                'type': 'multiple_choice',
                'options': ['Never', 'Once a year', '2-5 times a year', '6-10 times a year', 'More than 10 times'],
                'required': True
            },
            {
                'question': 'Have you flown with Kenya Airways before?',
                'type': 'yes_no',
                'required': True
            },
            {
                'question': 'How satisfied are you with Kenya Airways\' overall service?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'How would you rate Kenya Airways\' in-flight service?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'How would you rate Kenya Airways\' check-in process?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'What is most important to you when choosing an airline?',
                'type': 'multiple_choice',
                'options': ['Price', 'Schedule', 'Service quality', 'Safety record', 'Loyalty program', 'Direct flights', 'Baggage allowance'],
                'required': True
            },
            {
                'question': 'What is your travel purpose?',
                'type': 'multiple_choice',
                'options': ['Business', 'Leisure', 'Family visit', 'Education', 'Medical', 'Other'],
                'required': True
            },
            {
                'question': 'How much do you typically spend on air travel per year?',
                'type': 'multiple_choice',
                'options': ['Less than Ksh 50,000', 'Ksh 50,000 - 100,000', 'Ksh 100,000 - 200,000', 'Ksh 200,000 - 500,000', 'More than Ksh 500,000'],
                'required': True
            },
            {
                'question': 'Have you experienced any issues with Kenya Airways flights?',
                'type': 'yes_no',
                'required': True
            },
            {
                'question': 'How important is on-time performance when choosing an airline?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'Do you use Kenya Airways\' loyalty program (Flying Blue)?',
                'type': 'yes_no',
                'required': True
            },
            {
                'question': 'How satisfied are you with Kenya Airways\' baggage handling?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'What class do you usually travel in?',
                'type': 'multiple_choice',
                'options': ['Economy', 'Premium Economy', 'Business Class', 'First Class'],
                'required': True
            },
            {
                'question': 'Would you recommend Kenya Airways to others?',
                'type': 'yes_no',
                'required': True
            }
        ],
        'Brookside Dairy': [
            {
                'question': 'How often do you consume dairy products?',
                'type': 'multiple_choice',
                'options': ['Daily', '2-3 times a week', 'Weekly', 'Monthly', 'Rarely'],
                'required': True
            },
            {
                'question': 'Which Brookside Dairy products do you consume most frequently?',
                'type': 'multiple_choice',
                'options': ['Brookside Fresh Milk', 'Brookside Yogurt', 'Brookside Cheese', 'Brookside Butter', 'Brookside Cream', 'Brookside Long Life Milk', 'Brookside Flavored Milk'],
                'required': True
            },
            {
                'question': 'How satisfied are you with Brookside Dairy product quality?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'Where do you usually purchase Brookside Dairy products?',
                'type': 'multiple_choice',
                'options': ['Supermarkets (Naivas, Carrefour, etc.)', 'Local shops', 'Brookside outlets', 'Online delivery', 'Dairy shops', 'Direct from farmers'],
                'required': True
            },
            {
                'question': 'How important is product freshness when buying dairy products?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'What is your preferred milk fat content?',
                'type': 'multiple_choice',
                'options': ['Full cream (3.25% fat)', 'Reduced fat (2% fat)', 'Low fat (1% fat)', 'Skim milk (0.1% fat)', 'No preference'],
                'required': True
            },
            {
                'question': 'How much do you typically spend on dairy products per week?',
                'type': 'multiple_choice',
                'options': ['Less than Ksh 200', 'Ksh 200 - 500', 'Ksh 500 - 1,000', 'Ksh 1,000 - 2,000', 'More than Ksh 2,000'],
                'required': True
            },
            {
                'question': 'Have you ever experienced any issues with Brookside Dairy products?',
                'type': 'yes_no',
                'required': True
            },
            {
                'question': 'If yes, what type of issues have you encountered?',
                'type': 'multiple_choice',
                'options': ['Spoiled/expired products', 'Poor taste quality', 'Packaging issues', 'Inconsistent availability', 'Price concerns', 'None'],
                'required': False
            },
            {
                'question': 'How important is brand reputation when choosing dairy products?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'What factors influence your choice of dairy products?',
                'type': 'text',
                'required': False
            },
            {
                'question': 'Do you prefer locally produced dairy products?',
                'type': 'yes_no',
                'required': True
            },
            {
                'question': 'How often do you check expiration dates on dairy products?',
                'type': 'multiple_choice',
                'options': ['Always', 'Most of the time', 'Sometimes', 'Rarely', 'Never'],
                'required': True
            },
            {
                'question': 'What is your household size?',
                'type': 'multiple_choice',
                'options': ['1-2 people', '3-4 people', '5-6 people', '7+ people'],
                'required': True
            },
            {
                'question': 'Would you recommend Brookside Dairy products to others?',
                'type': 'yes_no',
                'required': True
            }
        ],
        'Jumia Kenya': [
            {
                'question': 'How often do you shop online?',
                'type': 'multiple_choice',
                'options': ['Daily', 'Weekly', 'Monthly', 'Rarely', 'Never'],
                'required': True
            },
            {
                'question': 'Have you used Jumia Kenya before?',
                'type': 'yes_no',
                'required': True
            },
            {
                'question': 'How satisfied are you with Jumia Kenya\'s overall service?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'How satisfied are you with Jumia\'s delivery service?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'What products do you usually buy from Jumia?',
                'type': 'text',
                'required': False
            },
            {
                'question': 'How much do you typically spend on online shopping per month?',
                'type': 'multiple_choice',
                'options': ['Less than Ksh 1,000', 'Ksh 1,000 - 5,000', 'Ksh 5,000 - 10,000', 'Ksh 10,000 - 20,000', 'More than Ksh 20,000'],
                'required': True
            },
            {
                'question': 'What is your preferred payment method for online shopping?',
                'type': 'multiple_choice',
                'options': ['M-PESA', 'Card payment', 'Cash on delivery', 'Bank transfer', 'Other'],
                'required': True
            },
            {
                'question': 'How important is delivery speed when shopping online?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'What improvements would you suggest for Jumia Kenya?',
                'type': 'text',
                'required': False
            },
            {
                'question': 'Would you recommend Jumia Kenya to others?',
                'type': 'yes_no',
                'required': True
            }
        ],
        'KCB Bank': [
            {
                'question': 'How long have you been a customer of KCB Bank?',
                'type': 'multiple_choice',
                'options': ['Less than 1 year', '1-3 years', '3-5 years', '5-10 years', 'More than 10 years'],
                'required': True
            },
            {
                'question': 'Which KCB Bank services do you use most frequently?',
                'type': 'multiple_choice',
                'options': ['Savings account', 'Current account', 'Loans', 'Mobile banking', 'Investment products', 'Credit cards', 'Insurance'],
                'required': True
            },
            {
                'question': 'How satisfied are you with KCB Bank\'s overall service?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'How would you rate KCB Bank\'s customer service?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'How satisfied are you with KCB Bank\'s mobile banking app?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'What improvements would you suggest for KCB Bank\'s mobile app?',
                'type': 'text',
                'required': False
            },
            {
                'question': 'How often do you visit a KCB Bank branch?',
                'type': 'multiple_choice',
                'options': ['Daily', 'Weekly', 'Monthly', 'Quarterly', 'Rarely'],
                'required': True
            },
            {
                'question': 'How much do you typically transact through KCB Bank per month?',
                'type': 'multiple_choice',
                'options': ['Less than Ksh 10,000', 'Ksh 10,000 - 50,000', 'Ksh 50,000 - 100,000', 'Ksh 100,000 - 500,000', 'More than Ksh 500,000'],
                'required': True
            },
            {
                'question': 'What is your occupation?',
                'type': 'multiple_choice',
                'options': ['Student', 'Employee', 'Business owner', 'Self-employed', 'Retired', 'Other'],
                'required': True
            },
            {
                'question': 'Would you recommend KCB Bank to others?',
                'type': 'yes_no',
                'required': True
            }
        ],
        'Twiga Foods': [
            {
                'question': 'How often do you purchase fresh produce?',
                'type': 'multiple_choice',
                'options': ['Daily', '2-3 times a week', 'Weekly', 'Bi-weekly', 'Monthly'],
                'required': True
            },
            {
                'question': 'Have you used Twiga Foods delivery service before?',
                'type': 'yes_no',
                'required': True
            },
            {
                'question': 'How satisfied are you with Twiga Foods product quality?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'How much do you typically spend on fresh produce per week?',
                'type': 'multiple_choice',
                'options': ['Less than Ksh 500', 'Ksh 500 - 1,000', 'Ksh 1,000 - 2,000', 'Ksh 2,000 - 5,000', 'More than Ksh 5,000'],
                'required': True
            },
            {
                'question': 'What factors influence your choice of fresh produce supplier?',
                'type': 'text',
                'required': False
            },
            {
                'question': 'Would you recommend Twiga Foods to others?',
                'type': 'yes_no',
                'required': True
            }
        ],
        'Co-operative Bank': [
            {
                'question': 'How long have you been a customer of Co-operative Bank?',
                'type': 'multiple_choice',
                'options': ['Less than 1 year', '1-3 years', '3-5 years', '5-10 years', 'More than 10 years'],
                'required': True
            },
            {
                'question': 'Which Co-operative Bank services do you use?',
                'type': 'multiple_choice',
                'options': ['Savings Account', 'Current Account', 'Loans', 'Mobile Banking', 'Internet Banking', 'Insurance', 'Investment Products'],
                'required': True
            },
            {
                'question': 'How satisfied are you with Co-operative Bank\'s customer service?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'How would you rate the convenience of Co-operative Bank\'s branch locations?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'Have you experienced any issues with Co-operative Bank\'s mobile banking app?',
                'type': 'yes_no',
                'required': True
            },
            {
                'question': 'How satisfied are you with Co-operative Bank\'s interest rates on savings?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'Would you recommend Co-operative Bank to friends and family?',
                'type': 'yes_no',
                'required': True
            },
            {
                'question': 'What improvements would you like to see in Co-operative Bank\'s services?',
                'type': 'text',
                'required': False
            },
            {
                'question': 'How likely are you to continue using Co-operative Bank in the next 2 years?',
                'type': 'multiple_choice',
                'options': ['Very Likely', 'Likely', 'Neutral', 'Unlikely', 'Very Unlikely'],
                'required': True
            }
        ],
        'Zuku': [
            {
                'question': 'How long have you been using Zuku internet services?',
                'type': 'multiple_choice',
                'options': ['Less than 6 months', '6 months - 1 year', '1-2 years', '2-5 years', 'More than 5 years'],
                'required': True
            },
            {
                'question': 'Which Zuku package do you currently subscribe to?',
                'type': 'multiple_choice',
                'options': ['Basic (5Mbps)', 'Standard (10Mbps)', 'Premium (20Mbps)', 'Ultra (40Mbps)', 'Fiber (100Mbps+)'],
                'required': True
            },
            {
                'question': 'How satisfied are you with Zuku\'s internet speed?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'How would you rate Zuku\'s customer service quality?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'Have you experienced frequent internet outages with Zuku?',
                'type': 'yes_no',
                'required': True
            },
            {
                'question': 'How satisfied are you with Zuku\'s pricing compared to other ISPs?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'Would you recommend Zuku to others?',
                'type': 'yes_no',
                'required': True
            }
        ],
        'Kipepeo Clothing': [
            {
                'question': 'How often do you shop for clothing?',
                'type': 'multiple_choice',
                'options': ['Weekly', 'Monthly', 'Every 2-3 months', 'Every 6 months', 'Yearly'],
                'required': True
            },
            {
                'question': 'Have you purchased from Kipepeo Clothing before?',
                'type': 'yes_no',
                'required': True
            },
            {
                'question': 'How satisfied are you with Kipepeo Clothing\'s product quality?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'How much do you typically spend on clothing per month?',
                'type': 'multiple_choice',
                'options': ['Less than Ksh 1,000', 'Ksh 1,000 - 3,000', 'Ksh 3,000 - 5,000', 'Ksh 5,000 - 10,000', 'More than Ksh 10,000'],
                'required': True
            },
            {
                'question': 'What factors influence your clothing purchase decisions?',
                'type': 'text',
                'required': False
            },
            {
                'question': 'Would you recommend Kipepeo Clothing to others?',
                'type': 'yes_no',
                'required': True
            }
        ],
        'KPLC': [
            {
                'question': 'How long have you been a KPLC customer?',
                'type': 'multiple_choice',
                'options': ['Less than 1 year', '1-3 years', '3-5 years', '5-10 years', 'More than 10 years'],
                'required': True
            },
            {
                'question': 'What type of KPLC connection do you have?',
                'type': 'multiple_choice',
                'options': ['Single Phase', 'Three Phase', 'Commercial', 'Industrial', 'Prepaid Meter'],
                'required': True
            },
            {
                'question': 'How satisfied are you with KPLC\'s electricity supply reliability?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'How often do you experience power outages?',
                'type': 'multiple_choice',
                'options': ['Never', 'Rarely (1-2 times/month)', 'Occasionally (3-5 times/month)', 'Frequently (6-10 times/month)', 'Very Frequently (10+ times/month)'],
                'required': True
            },
            {
                'question': 'How satisfied are you with KPLC\'s customer service?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'How would you rate KPLC\'s billing accuracy?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'Have you reported any issues to KPLC in the past 6 months?',
                'type': 'yes_no',
                'required': True
            },
            {
                'question': 'How satisfied are you with KPLC\'s response time to outages?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'How much do you typically spend on electricity per month?',
                'type': 'multiple_choice',
                'options': ['Less than Ksh 1,000', 'Ksh 1,000 - 3,000', 'Ksh 3,000 - 5,000', 'Ksh 5,000 - 10,000', 'More than Ksh 10,000'],
                'required': True
            },
            {
                'question': 'What improvements would you like to see in KPLC\'s services?',
                'type': 'text',
                'required': False
            },
            {
                'question': 'Would you recommend KPLC to others?',
                'type': 'yes_no',
                'required': True
            }
        ],
        'Bidco Africa': [
            {
                'question': 'How long have you been using Bidco Africa products?',
                'type': 'multiple_choice',
                'options': ['Less than 6 months', '6 months - 1 year', '1-2 years', '2-5 years', 'More than 5 years'],
                'required': True
            },
            {
                'question': 'Which Bidco Africa products do you use?',
                'type': 'multiple_choice',
                'options': ['Cooking Oil', 'Soap & Detergents', 'Personal Care', 'Food Products', 'Industrial Products', 'All of the above'],
                'required': True
            },
            {
                'question': 'How satisfied are you with Bidco Africa\'s product quality?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'How often do you purchase Bidco Africa products?',
                'type': 'multiple_choice',
                'options': ['Daily', 'Weekly', 'Monthly', 'Every 2-3 months', 'Occasionally'],
                'required': True
            },
            {
                'question': 'How satisfied are you with Bidco Africa\'s pricing?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'Have you experienced any issues with Bidco Africa products?',
                'type': 'yes_no',
                'required': True
            },
            {
                'question': 'How would you rate Bidco Africa\'s product availability in stores?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'How much do you typically spend on Bidco Africa products per month?',
                'type': 'multiple_choice',
                'options': ['Less than Ksh 500', 'Ksh 500 - 1,000', 'Ksh 1,000 - 2,000', 'Ksh 2,000 - 5,000', 'More than Ksh 5,000'],
                'required': True
            },
            {
                'question': 'How satisfied are you with Bidco Africa\'s packaging?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'Would you recommend Bidco Africa products to others?',
                'type': 'yes_no',
                'required': True
            },
            {
                'question': 'What improvements would you like to see in Bidco Africa products?',
                'type': 'text',
                'required': False
            },
            {
                'question': 'How likely are you to continue using Bidco Africa products?',
                'type': 'multiple_choice',
                'options': ['Very Likely', 'Likely', 'Neutral', 'Unlikely', 'Very Unlikely'],
                'required': True
            }
        ],
        'Safaricom Home Fibre': [
            {
                'question': 'How long have you been using Safaricom Home Fibre?',
                'type': 'multiple_choice',
                'options': ['Less than 6 months', '6 months - 1 year', '1-2 years', '2-5 years', 'More than 5 years'],
                'required': True
            },
            {
                'question': 'Which Safaricom Home Fibre package do you subscribe to?',
                'type': 'multiple_choice',
                'options': ['8Mbps', '16Mbps', '25Mbps', '40Mbps', '100Mbps', '200Mbps'],
                'required': True
            },
            {
                'question': 'How satisfied are you with Safaricom Home Fibre\'s internet speed?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'How often do you experience internet connectivity issues?',
                'type': 'multiple_choice',
                'options': ['Never', 'Rarely (1-2 times/month)', 'Occasionally (3-5 times/month)', 'Frequently (6-10 times/month)', 'Very Frequently (10+ times/month)'],
                'required': True
            },
            {
                'question': 'How satisfied are you with Safaricom Home Fibre\'s customer service?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'How would you rate Safaricom Home Fibre\'s installation process?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'Have you contacted Safaricom Home Fibre support in the past 6 months?',
                'type': 'yes_no',
                'required': True
            },
            {
                'question': 'How satisfied are you with Safaricom Home Fibre\'s pricing?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'What improvements would you like to see in Safaricom Home Fibre services?',
                'type': 'text',
                'required': False
            },
            {
                'question': 'Would you recommend Safaricom Home Fibre to others?',
                'type': 'yes_no',
                'required': True
            }
        ],
        'Artcaffe': [
            {
                'question': 'How often do you visit Artcaffe?',
                'type': 'multiple_choice',
                'options': ['Daily', '2-3 times a week', 'Weekly', 'Monthly', 'Occasionally'],
                'required': True
            },
            {
                'question': 'What is your primary reason for visiting Artcaffe?',
                'type': 'multiple_choice',
                'options': ['Coffee/Tea', 'Food/Meals', 'Work/Study', 'Socializing', 'Business Meetings', 'All of the above'],
                'required': True
            },
            {
                'question': 'How satisfied are you with Artcaffe\'s food quality?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'How satisfied are you with Artcaffe\'s coffee quality?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'How would you rate Artcaffe\'s service speed?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'How satisfied are you with Artcaffe\'s pricing?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'How would you rate Artcaffe\'s ambiance and atmosphere?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'How much do you typically spend per visit to Artcaffe?',
                'type': 'multiple_choice',
                'options': ['Less than Ksh 500', 'Ksh 500 - 1,000', 'Ksh 1,000 - 2,000', 'Ksh 2,000 - 5,000', 'More than Ksh 5,000'],
                'required': True
            },
            {
                'question': 'Have you experienced any issues with Artcaffe\'s service?',
                'type': 'yes_no',
                'required': True
            },
            {
                'question': 'How satisfied are you with Artcaffe\'s staff friendliness?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'What improvements would you like to see at Artcaffe?',
                'type': 'text',
                'required': False
            },
            {
                'question': 'Would you recommend Artcaffe to others?',
                'type': 'yes_no',
                'required': True
            }
        ]
    }
    
    # Get questions for the specific survey, or use a default set
    if survey_title in question_templates:
        questions = question_templates[survey_title]
    else:
        # Default questions for any survey
        default_questions = [
            {
                'question': 'How satisfied are you with this service?',
                'type': 'rating',
                'scale': 5,
                'required': True
            },
            {
                'question': 'Would you recommend this service to others?',
                'type': 'yes_no',
                'required': True
            },
            {
                'question': 'What aspects could be improved?',
                'type': 'text',
                'required': False
            },
            {
                'question': 'How did you hear about this service?',
                'type': 'multiple_choice',
                'options': ['Social media', 'Friend recommendation', 'Advertisement', 'Search engine', 'Other'],
                'required': True
            },
            {
                'question': 'What is your age group?',
                'type': 'multiple_choice',
                'options': ['18-25', '26-35', '36-45', '46-55', '55+'],
                'required': True
            }
        ]
        questions = random.sample(default_questions, min(5, len(default_questions)))
    
    # Add question numbers
    for i, question in enumerate(questions, 1):
        question['number'] = i
    
    return questions

def home(request):
    testimonials = [
        {
            'name': 'Sarah Johnson',
            'role': 'Student',
            'quote': 'PennySurveys has become my go-to platform for earning extra money during my studies. The surveys are engaging and the payments are always on time!',
        },
        {
            'name': 'James Mwangi',
            'role': 'Entrepreneur',
            'quote': 'I love how easy it is to use PennySurveys. The interface is user-friendly and the rewards are real!',
        },
        {
            'name': 'Amina Yusuf',
            'role': 'Freelancer',
            'quote': 'Quick payouts and interesting surveys! I recommend PennySurveys to anyone looking to earn online.',
        },
        {
            'name': 'Wanjiku Maina',
            'role': 'Illustrative example | Graduate student',
            'quote': 'I can scan survey topics quickly and choose one that fits the time I have.',
        },
        {
            'name': 'Esther Njoroge',
            'role': 'Illustrative example | Small business owner',
            'quote': 'Short surveys are easy to fit into a busy day when I have a few spare minutes.',
        },
        {
            'name': 'Collins Were',
            'role': 'Illustrative example | Retail assistant',
            'quote': 'I like seeing the reward and estimated time before starting a survey.',
        },
        {
            'name': 'Lucy Wairimu',
            'role': 'Illustrative example | Freelance designer',
            'quote': 'The simple layout helps me find available surveys without much searching.',
        },
        {
            'name': 'Peter Kirui',
            'role': 'Illustrative example | Customer support agent',
            'quote': 'I use the site in the evening when I have a little time to spare.',
        },
        {
            'name': 'Irene Wambua',
            'role': 'Illustrative example | Accountant',
            'quote': 'The different survey topics help keep the experience interesting.',
        },
        {
            'name': 'Victor Kariuki',
            'role': 'Illustrative example | Teacher',
            'quote': 'It is useful to have my progress and available surveys together in one place.',
        },
        {
            'name': 'Grace Muthoni',
            'role': 'Illustrative example | Sales associate',
            'quote': 'I can check the dashboard and see which surveys are ready to take.',
        },
        {
            'name': 'Samuel Maina',
            'role': 'Illustrative example | University student',
            'quote': 'The instructions help me know what to expect before I begin a survey.',
        },
        {
            'name': 'Diana Cherono',
            'role': 'Illustrative example | Self-employed',
            'quote': 'It is a straightforward way to share feedback in my spare time.',
        },
    ]
    return render(request, 'surveys/index.html', {'testimonials': testimonials})

def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'surveys/register.html', {'form': form})

def dashboard(request):
    full_name = None
    total_earnings = 0.00
    surveys_completed = 0
    if request.user.is_authenticated:
        try:
            profile = request.user.userprofile
            full_name = profile.full_name
            total_earnings = getattr(profile, 'total_earnings', 0.00)
            surveys_completed = getattr(profile, 'surveys_completed', 0)
        except UserProfile.DoesNotExist:
            full_name = request.user.username
            total_earnings = 0.00
            surveys_completed = 0
        except Exception as e:
            # Handle case where migration hasn't been applied yet
            full_name = request.user.username
            total_earnings = 0.00
            surveys_completed = 0
    return render(request, 'surveys/dashboard.html', {
        'full_name': full_name,
        'total_earnings': total_earnings,
        'surveys_completed': surveys_completed,
        'show_sidebar': True
    })

def settings_view(request):
    profile = None
    if request.user.is_authenticated:
        try:
            profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            profile = None
    return render(request, 'surveys/settings.html', {
        'profile': profile,
        'show_sidebar': True
    })

def add_mpesa_number(request):
    next_url = request.GET.get('next', 'dashboard')
    if request.method == 'POST' and request.user.is_authenticated:
        mpesa_number = request.POST.get('mpesa_number')
        if mpesa_number:
            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            profile.mpesa_number = mpesa_number
            profile.save()
        return redirect(next_url)
    return redirect(next_url)

@login_required
def surveys_list(request):
    # Get user profile to check if they've taken their first survey
    try:
        profile = request.user.userprofile
        has_taken_first_survey = getattr(profile, 'has_taken_first_survey', False)
        system_survey_attempts = getattr(profile, 'system_survey_attempts', 0)
        print(f"Surveys list - User: {request.user.username}, Has taken first survey: {has_taken_first_survey}")
    except UserProfile.DoesNotExist:
        profile = None
        has_taken_first_survey = False
        system_survey_attempts = 0
        print(f"Surveys list - User: {request.user.username}, No profile found")
    except Exception as e:
        # Handle case where migration hasn't been applied yet
        profile = None
        has_taken_first_survey = False
        system_survey_attempts = 0
        print(f"Surveys list - User: {request.user.username}, Exception: {e}")
    max_system_survey_attempts = 2
    system_survey_attempts_remaining = max(max_system_survey_attempts - system_survey_attempts, 0)
    
    # Clean surveys list - System survey first, then paid surveys (no duplicates)
    surveys = [
        {
            'title': 'SurveysPlus',
            'questions': 7,
            'reward': 160,
            'type': 'system',
            'status': 'always',
            'estimated_time': 11,
            'button_color': 'success',
            'button_text': 'Take Survey',
            'highlight': 'green',
        },
        {
            'title': 'Safaricom M-PESA',
            'questions': 15,
            'reward': 210,
            'type': 'paid',
            'status': 'paid',
            'estimated_time': 15,
            'button_color': 'primary',
            'button_text': 'Take Survey',
            'highlight': 'yellow',
        },
        {
            'title': 'Kenya Airways',
            'questions': 13,
            'reward': 260,
            'type': 'paid',
            'status': 'paid',
            'estimated_time': 15,
            'button_color': 'primary',
            'button_text': 'Take Survey',
            'highlight': 'yellow',
        },
        {
            'title': 'Naivas Supermarket',
            'questions': 10,
            'reward': 120,
            'type': 'paid',
            'status': 'paid',
            'estimated_time': 12,
            'button_color': 'primary',
            'button_text': 'Take Survey',
            'highlight': 'yellow',
        },
        {
            'title': 'Jumia Kenya',
            'questions': 10,
            'reward': 180,
            'type': 'paid',
            'status': 'paid',
            'estimated_time': 12,
            'button_color': 'primary',
            'button_text': 'Take Survey',
            'highlight': 'yellow',
        },
        {
            'title': 'KCB Bank',
            'questions': 10,
            'reward': 170,
            'type': 'paid',
            'status': 'paid',
            'estimated_time': 12,
            'button_color': 'primary',
            'button_text': 'Take Survey',
            'highlight': 'yellow',
        },
        {
            'title': 'Equity Bank',
            'questions': 10,
            'reward': 140,
            'type': 'paid',
            'status': 'paid',
            'estimated_time': 12,
            'button_color': 'primary',
            'button_text': 'Take Survey',
            'highlight': 'yellow',
        },
        {
            'title': 'Brookside Dairy',
            'questions': 15,
            'reward': 100,
            'type': 'paid',
            'status': 'paid',
            'estimated_time': 12,
            'button_color': 'primary',
            'button_text': 'Take Survey',
            'highlight': 'yellow',
        },
        {
            'title': 'Twiga Foods',
            'questions': 6,
            'reward': 130,
            'type': 'paid',
            'status': 'paid',
            'estimated_time': 9,
            'button_color': 'primary',
            'button_text': 'Take Survey',
            'highlight': 'yellow',
        },
        {
            'title': 'Co-operative Bank',
            'questions': 9,
            'reward': 110,
            'type': 'paid',
            'status': 'paid',
            'estimated_time': 8,
            'button_color': 'primary',
            'button_text': 'Take Survey',
            'highlight': 'yellow',
        },
        {
            'title': 'Zuku',
            'questions': 7,
            'reward': 190,
            'type': 'paid',
            'status': 'paid',
            'estimated_time': 11,
            'button_color': 'primary',
            'button_text': 'Take Survey',
            'highlight': 'yellow',
        },
        {
            'title': 'Kipepeo Clothing',
            'questions': 6,
            'reward': 125,
            'type': 'paid',
            'status': 'paid',
            'estimated_time': 9,
            'button_color': 'primary',
            'button_text': 'Take Survey',
            'highlight': 'yellow',
        },
        {
            'title': 'KPLC',
            'questions': 11,
            'reward': 150,
            'type': 'paid',
            'status': 'paid',
            'estimated_time': 9,
            'button_color': 'primary',
            'button_text': 'Take Survey',
            'highlight': 'yellow',
        },
        {
            'title': 'Bidco Africa',
            'questions': 12,
            'reward': 115,
            'type': 'paid',
            'status': 'paid',
            'estimated_time': 8,
            'button_color': 'primary',
            'button_text': 'Take Survey',
            'highlight': 'yellow',
        },
        {
            'title': 'Safaricom Home Fibre',
            'questions': 10,
            'reward': 220,
            'type': 'paid',
            'status': 'paid',
            'estimated_time': 11,
            'button_color': 'primary',
            'button_text': 'Take Survey',
            'highlight': 'yellow',
        },
        {
            'title': 'Artcaffe',
            'questions': 12,
            'reward': 145,
            'type': 'paid',
            'status': 'paid',
            'estimated_time': 10,
            'button_color': 'primary',
            'button_text': 'Take Survey',
            'highlight': 'yellow',
        }
    ]
    # Get subscription status
    has_active_subscription = getattr(profile, 'has_active_subscription', False) if profile else False
    
    return render(request, 'surveys/surveys.html', {
        'surveys': surveys,
        'show_sidebar': True,
        'has_taken_first_survey': has_taken_first_survey,
        'has_active_subscription': has_active_subscription,
        'system_survey_attempts': system_survey_attempts,
        'system_survey_attempts_remaining': system_survey_attempts_remaining,
    })

@login_required
def take_survey(request, survey_title):
    """Handle taking a survey with subscription logic"""
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    except Exception as e:
        profile = UserProfile.objects.create(user=request.user)

    # Check if user has taken their first survey and has active subscription
    has_taken_first_survey = getattr(profile, 'has_taken_first_survey', False)
    has_active_subscription = getattr(profile, 'has_active_subscription', False)
    system_survey_attempts = getattr(profile, 'system_survey_attempts', 0)
    max_system_survey_attempts = 2

    # Only "SurveysPlus" is always free, all others require subscription after first survey
    if survey_title != 'SurveysPlus' and has_taken_first_survey and not has_active_subscription:
        # Redirect to subscriptions for paid surveys
        return redirect(f'/subscriptions/?survey={survey_title}')

    if survey_title == 'SurveysPlus' and system_survey_attempts >= max_system_survey_attempts:
        messages.error(request, 'This survey is available only twice per user. You have reached the limit.')
        return redirect('surveys_list')

    if request.method == 'GET':
        survey_data = get_survey_data(survey_title)
        return render(request, 'surveys/survey_instructions.html', {
            'survey_title': survey_title,
            'survey_reward': survey_data['reward'],
            'survey_time': survey_data['estimated_time'],
            'survey_questions': survey_data['questions'],
            'show_sidebar': True
        })
    elif request.method == 'POST':
        if 'start_survey' in request.POST:
            questions = generate_survey_questions(survey_title)
            return render(request, 'surveys/take_survey.html', {
                'survey_title': survey_title,
                'questions': questions,
                'show_sidebar': True
            })
        else:
            # Process survey submission
            try:
                # Get survey data to find the reward amount
                survey_data = get_survey_data(survey_title)
                survey_reward = survey_data['reward']
                
                # Update user profile
                profile.has_taken_first_survey = True
                profile.total_earnings += survey_reward
                profile.surveys_completed += 1
                if survey_title == 'SurveysPlus':
                    profile.system_survey_attempts += 1
                profile.save()
                
                print(f"Marked {request.user.username} as having taken first survey")
                print(f"Added Ksh {survey_reward} to total earnings. New total: Ksh {profile.total_earnings}")
                
                messages.success(request, f'Congratulations! You completed "{survey_title}" and earned Ksh {survey_reward}!')
            except Exception as e:
                print(f"Error updating user profile: {e}")
                messages.success(request, f'Congratulations! You completed "{survey_title}"!')
            
            return redirect('surveys_list')

def subscriptions(request):
    # Get the survey title from the URL parameter
    survey_title = request.GET.get('survey', '')
    
    plans = [
        {
            'name': 'Business Basic',
            'price': 150,
            'per': 'month',
            'features': [
                '5 surveys per day',
                'Ksh 8,000 monthly income',
                'Ksh 500 daily income',
                'Ksh 3,000 min. withdrawal',
                'Ksh 50 - 100 per survey',
            ],
            'highlight': 'basic',
            'button_color': 'primary',
            'popular': False,
        },
        {
            'name': 'Business Premium',
            'price': 300,
            'per': 'month',
            'features': [
                '10 surveys per day',
                'Ksh 15,000 monthly income',
                'Ksh 1,000 daily income',
                'Ksh 2,500 min. withdrawal',
                'Ksh 50 - 100 per survey',
            ],
            'highlight': 'premium',
            'button_color': 'gradient',
            'popular': True,
        },
        {
            'name': 'Business Expert',
            'price': 500,
            'per': 'month',
            'features': [
                '20 surveys per day',
                'Ksh 30,000 monthly income',
                'Ksh 2,000 daily income',
                'Ksh 2,000 min. withdrawal',
                'Ksh 50 - 100 per survey',
            ],
            'highlight': 'expert',
            'button_color': 'primary',
            'popular': False,
        },
    ]
    return render(request, 'surveys/subscriptions.html', {
        'plans': plans, 
        'show_sidebar': True,
        'survey_title': survey_title
    })

def subscription_payment(request: HttpRequest):
    if request.method == 'POST':
        # Handle payment confirmation
        mpesa_message = request.POST.get('mpesa_message')
        survey_title = request.POST.get('survey_title', '')
        plan = request.POST.get('plan', 'Business Basic')
        amount = request.POST.get('amount', '300')
        
        if mpesa_message:
            # Validate that the M-PESA message contains "NAVARA SOLUTIONS"
            if 'NAVARA SOLUTIONS' not in mpesa_message.upper():
                return render(request, 'surveys/subscription_payment.html', {
                    'plan': plan,
                    'amount': amount,
                    'till_number': '5671240',
                    'survey_title': survey_title,
                    'show_sidebar': True,
                    'error_message': 'Please paste the correct M-PESA message!',
                    'mpesa_message': mpesa_message  # Preserve the entered message
                })
            
            # In a real app, you would verify the M-PESA message here
            # For now, we'll just mark the user as having an active subscription
            try:
                profile = request.user.userprofile
                profile.has_active_subscription = True
                profile.save()
                print(f"Marked {request.user.username} as having active subscription")
            except Exception as e:
                print(f"Error setting has_active_subscription: {e}")
            
            messages.success(request, 'Payment confirmed! You now have access to all paid surveys.')
            return redirect('surveys_list')
        else:
            return render(request, 'surveys/subscription_payment.html', {
                'plan': plan,
                'amount': amount,
                'till_number': '5671240',
                'survey_title': survey_title,
                'show_sidebar': True,
                'error_message': 'Please enter a valid M-PESA message.'
            })
    
    plan = request.GET.get('plan', 'Business Basic')
    amount = request.GET.get('amount', '300')
    survey_title = request.GET.get('survey', '')
    till_number = '5671240'
    return render(request, 'surveys/subscription_payment.html', {
        'plan': plan,
        'amount': amount,
        'till_number': till_number,
        'survey_title': survey_title,
        'show_sidebar': True
    })

@login_required
def withdraw_funds(request):
    """Handle withdraw funds page"""
    return render(request, 'surveys/withdraw_funds.html', {
        'show_sidebar': True
    })

@login_required
def change_password(request):
    """Handle password change functionality"""
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        # Check if current password is correct
        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('settings')
        
        # Check if new passwords match
        if new_password1 != new_password2:
            messages.error(request, 'New passwords do not match.')
            return redirect('settings')
        
        # Check password length
        if len(new_password1) < 8:
            messages.error(request, 'New password must be at least 8 characters long.')
            return redirect('settings')
        
        # Check if new password is different from current
        if current_password == new_password1:
            messages.error(request, 'New password must be different from current password.')
            return redirect('settings')
        
        # Change the password
        try:
            request.user.set_password(new_password1)
            request.user.save()
            messages.success(request, 'Password changed successfully! Please log in again.')
            return redirect('login')
        except Exception as e:
            messages.error(request, 'An error occurred while changing password. Please try again.')
            return redirect('settings')
    
    return redirect('settings')
