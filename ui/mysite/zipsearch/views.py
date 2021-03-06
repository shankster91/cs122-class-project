from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django import forms
import os
import csv

COLUMN_NAMES = dict(
    zip='Zip Code',
    target_state='Target State'
)

PREF_COLS = {
    'Demographics': 'census',
    'Business': 'business_count',
    'Schools': 'great_schools',
    'Political Ideology': 'ideology',
    'Libraries': 'libraries',
    'Museums': 'museums',
    'Walk Score': 'walk_score',
    'Weather': 'weather',
    'Housing Prices': 'zillow'
}

RES_DIR = os.path.join(os.path.dirname(__file__), '..', 'res')

def _build_dropdown(options):
    """Convert a list to (value, caption) tuples."""
    return [(x, x) for x in options]

def _load_column(filename, col=0):
    """Load single column from csv file."""
    with open(filename) as f:
        col = list(zip(*csv.reader(f)))[0]
        return list(col)

def _load_res_column(filename, col=0):
    """Load column from resource directory."""
    return _load_column(os.path.join(RES_DIR, filename), col=col)

ZIPS = _build_dropdown(_load_res_column('zip_list.csv'))
STATES = _build_dropdown(_load_res_column('state_list.csv'))
PREFS = _build_dropdown(_load_res_column('pref_list.csv'))

class SearchForm(forms.Form):
    zips = forms.ChoiceField(
        label='Zip Code',
        choices=ZIPS,
        help_text='Select a zip code you want to compare to',
        required=False)
    state = forms.ChoiceField(
        label='Target State',
        choices=STATES,
        help_text='Select a state to look for similar zip codes',
        required=False)
    prefs = forms.MultipleChoiceField(label='Preferences',
                                     choices=PREFS,
                                     help_text='Select the data you would like to match on. You must choose at least one.',
                                     widget=forms.CheckboxSelectMultiple(attrs={"checked":""}))

def index(request):
    #template = loader.get_template('zipsearch/index.html')
    #return render(request, 'zipsearch/index.html')
    #return HttpResponse(template.render(request))
    context = {}
    args = {}
    res = None
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.GET or None)
        # check whether it's valid:
        if form.is_valid():

            # Convert form data to an args dictionary for find_courses
            input_zip = form.cleaned_data['zips']
            if input_zip != '':
                args['input_zip'] = int(input_zip)
            args['input_state'] = form.cleaned_data['state']
            tables = []
            for val in form.cleaned_data['prefs']:
                tables.append(PREF_COLS[val])
            args['tables'] = tables
#             if form.cleaned_data['show_args']:
#                 context['args'] = 'args_to_ui = ' + json.dumps(args, indent=2)

#             try:
#                 res = find_courses(args)
#             except Exception as e:
#                 print('Exception caught')
#                 bt = traceback.format_exception(*sys.exc_info()[:3])
#                 context['err'] = """
#                 An exception was thrown in find_courses:
#                 <pre>{}
# {}</pre>
#                 """.format(e, '\n'.join(bt))

#                 res = None
        #else:
            #raise forms.ValidationError("Select at least one preference.")
    else:
        #form = SearchForm()
        #print("invalid")
        pass

    # # Handle different responses of res
    # if res is None:
    #     context['result'] = None
    # elif isinstance(res, str):
    #     context['result'] = None
    #     context['err'] = res
    #     result = None
    # elif not _valid_result(res):
    #     context['result'] = None
    #     context['err'] = ('Return of find_courses has the wrong data type. '
    #                       'Should be a tuple of length 4 with one string and '
    #                       'three lists.')
    # else:
    #     columns, result = res

    #     # Wrap in tuple if result is not already
    #     if result and isinstance(result[0], str):
    #         result = [(r,) for r in result]

    #     context['result'] = result
    #     context['num_results'] = len(result)
    #context['columns'] = [COLUMN_NAMES.get(col, col) for col in columns]

    context['form'] = form
    print(args)
    return render(request, 'zipsearch/index.html', context)