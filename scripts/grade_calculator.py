import pandas 
import argparse

DEBUG = 0

def get_categories(data):
   '''
   finds all unique categories for grading
   return dictionary
   '''

   cats = {}
   for i, c in enumerate(data['category']):
      if c not in cats:
         cats[c] = data['percentage'][i]

   return cats

def check_cats(categories):
   '''
   checks that percentages sum to 100
   categories is a dictionary
   key is category value is percentage
   '''

   total = 0
   for value in categories.values():
      total += value 

   if total != 100:
      return True

   return False

def get_grades(data, categories):
   '''
   calculates current grades for each category and returns dictionary
   data -> input data from csv
   categories -> grade categories possible
   '''

   grades = {}

   # get grades for each category
   for category in categories.keys():
      grade_values = data.loc[data['category'] == category]

      # print(grade_values)

      score = 0
      total = 0

      for i, g in grade_values.iterrows():
         if g['grade'] == '?' or g['total'] == '?':
            continue

         score += float(g['grade'])
         total += float(g['total'])

      if total > 0:
         grades[category] = score / total
      else:
         grades[category] = 0

   return grades

def calc_grade(categories, grades):
   ''' 
   categories -> dictionary with grade categories and percentages 
   grades -> dictionary with grade categories and grades for each
   calculates final grade and returns float value
   '''

   final = 0.0
   cat = None
   for category, percentage in categories.items():
      if grades[category] == 0:
         cat = category

      g_per_cat = grades[category] * percentage
      final += g_per_cat

   return final, cat

def estimate_grade(percentage, final_grade, min_val):
   '''
   check -> category needed to estimate grade for 
   grades -> dictionary with grades per category 
   final_grade -> float type of current grade 
   min_val -> minimum value to estimate for 
   '''

   estimate = 0
   final = 0
   while final < min_val:
      estimate += 1
      final = final_grade + (estimate * percentage)      

   return estimate, final
   
def print_dict(dictionary):
   '''
   prints dictionary
   '''
   
   for key, value in dictionary.items():
      print(key, value)
   print()

   return

def grade_solver(args):
   # read csv file
   # csv file has columns: category, grade, total, percentage
   data = pandas.read_csv(args.grades)
   
   if data.empty:
      print('file not read. exiting')
      exit()

   # get categories for grading
   categories = get_categories(data)
   error = check_cats(categories)

   if error:
      print('percentage totals do not sum to 100. exiting')
      exit()

   if DEBUG:
      print_dict(categories)

   # add individual grades per category
   grades = get_grades(data, categories)

   if len(grades) == 0:
      print('no grades found. exiting')
      exit()

   if DEBUG:
      print_dict(grades)

   # calculate final grade and check if grade is missing
   final_grade, check = calc_grade(categories, grades)
   print()
   print('final grade = ' + str(final_grade))

   # if grade missing calculate theoretical grade needed
   if check:
      percentage = categories[check] / 100
      grade_needed, theoretical = estimate_grade(percentage, final_grade, args.min_val)
   
      print('grade needed for ' + check + ' = ' + str(grade_needed))
      print('theoretical final grade = ' + str(theoretical))

   return

if __name__ == '__main__':
   parser = argparse.ArgumentParser()
   parser.add_argument('--grades', type=str, help='csv file with grades')
   parser.add_argument('--min-val', type=int, help='lowest grade needed', default=80)

   args = parser.parse_args()
   grade_solver(args)