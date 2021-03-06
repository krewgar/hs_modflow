from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import Button, SelectInput, TextInput
from .model import save_hs_to_favorites, get_all_models, upload_to_hs

@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    upload_button = Button(
        display_text='Upload to Hydroshare',
        name='upload-button',
        attributes={
            'data-toggle':'modal',
            'data-target':'#upload-modal',
            'data-placement': 'top',
            'title':'Upload'
        }
    )

    download_button = Button(
        display_text='Download from Hydroshare',
        name='edit-button',
        attributes={
            'data-toggle':'modal',
            'data-target':'#download-modal',
            'data-placement': 'top',
            'title':'Download'
        }
    )

    run_button = Button(
        display_text='Run Model',
        name='run-button',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Run Model',
            'onclick':'run_model ()'
        }
    )

    load_button = Button(
        display_text='Load Model',
        name='load-button',
        attributes={
            'data-toggle': 'tooltip',
            'data-placement': 'top',
            'title': 'Load Model',
            'onclick': 'load_model ()'
        }
    )

    edit_button = Button(
        display_text='',
        name='edit-button',
        icon='glyphicon glyphicon-edit',
        style='warning',
        attributes={
            'data-toggle': 'tooltip',
            'data-placement': 'top',
            'title': 'Edit Text',
            'align': 'left',
            'onclick': 'enable_text_edit ()'
        }
    )

    save_text_button = Button(
        display_text='',
        name='save-text-button',
        icon='glyphicon glyphicon-floppy-disk',
        style='success',
        attributes={
            'data-toggle':'modal',
            'data-target':'#save-modal',
            'data-placement':'top',
            'title':'Save Text',
        }
    )

    overwrite_button = Button(
        display_text='Overwrite',
        name='overwrite-button',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Overwrite Existing',
            'onclick': 'save_text_files ()'
        }
    )

    new_entry_button = Button(
        display_text='Save As New Entry',
        name='new-entry-button',
        attributes={
            'data-toggle':'modal',
            'data-target':'#new-entry-modal',
            'data-placement':'top',
            'title':'Save As New Entry',
        }
    )

    dont_save_button = Button(
        display_text='Dont Save',
        name='dont-save-button',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Dont Save',
            'onclick': 'hideOverwriteModal ()'
        }
    )

    new_display_name_input = TextInput(display_text='New Display Name',
                           name='new_display_name_input',
                           placeholder='')

    modellist = get_all_models()

    model_select = SelectInput(display_text='Select a Model',
                                name='model_select',
                                multiple=False,
                                options=modellist,
                                select2_options={'placeholder': 'Select a number',
                                                 'allowClear': False})

    modeltype_select = SelectInput(display_text='Select Model Type',
                               name='modeltype_select',
                               multiple=False,
                               options=[('Modflow 2005', 'mf2005'), ('Modflow-NWT', 'mfnwt')],
                               select2_options={'placeholder': 'Select a Model Type',
                                                'allowClear': False})

    resourceid_input = TextInput(display_text='Resource ID',
                                name='resourceid_input',
                                placeholder='')

    search_input = TextInput(display_text='Search',
                           name='search_input',
                           placeholder="comma,separated,list,of,subjects")

    resourcedisplay_input = TextInput(display_text='Resource Display Name for Favorite Select',
                                 name='resourcedisplay_input',
                                 placeholder='')

    # Default Values
    resourceid = ''
    displayname = ''
    modeltype = ''

    # Errors
    resourceid_error = ''
    displayname_error = ''
    modeltype_error = ''

    # Handle form submission
    if request.POST and 'download-button' in request.POST:
        # Get values
        has_errors = False
        resourceid = request.POST.get('resourceid_input', None)
        displayname = request.POST.get('resourcedisplay_input', None)
        modeltype = request.POST.get('modeltype_select', None)

        # Validate
        if not resourceid:
            has_errors = True
            resourceid_error = 'Name is required.'

        if not displayname:
            has_errors = True
            displayname_error = 'Owner is required.'

        if not modeltype:
            has_errors = True
            modeltype_error = 'River is required.'

        if not has_errors:
            save_hs_to_favorites(resourceid,displayname,modeltype)
            return redirect(reverse('hs_modflow:home'))

        messages.error(request, "Please fix errors.")

    resourcename_input = TextInput(display_text='Resource Name',
                                 name='resource_name',
                                 placeholder='')

    resourcekey_input = TextInput(display_text='Resource Keywords',
                                 name='resource_key',
                                 placeholder='')

    resourceabstract_input = TextInput(display_text='Resource Abstract',
                                 name='resource_abstract',
                                 placeholder='')


    # Default Values
    uploadtype = ''
    modelname = ''

    # Errors
    uploadtype_error = ''
    modelname_error = ''

    # Handle form submission
    if request.POST and 'upload-button' in request.POST:
        # Get values
        has_errors = False
        uploadtype = request.POST.get('uploadtype', None)
        modelname = request.POST.get('model_select', None)
        resource_name = request.POST.get('resource_name', None)
        resource_abstract = request.POST.get('resource_abstract', None)
        resource_key = request.POST.get('resource_key', None)

        # Validate
        if not uploadtype:
            has_errors = True
            uploadtype_error = 'Upload Option is required.'

        if not modelname:
            has_errors = True
            modelname_error = 'Model is required.'

        if not has_errors:
            upload_to_hs(uploadtype, modelname, resource_name, resource_abstract, resource_key)
            return redirect(reverse('hs_modflow:home'))

        messages.error(request, "Please fix errors.")

    context = {
        'overwrite_button': overwrite_button,
        'new_entry_button': new_entry_button,
        'dont_save_button': dont_save_button,
        'edit_button': edit_button,
        'save_text_button': save_text_button,
        'new_display_name_input': new_display_name_input,
        'upload_button': upload_button,
        'download_button': download_button,
        'load_button': load_button,
        'run_button': run_button,
        'model_select': model_select,
        'modeltype_select':modeltype_select,
        'resourceid_input':resourceid_input,
        'search_input':search_input,
        'resourcedisplay_input':resourcedisplay_input,
        'resourcename_input':resourcename_input,
        'resourceabstract_input':resourceabstract_input,
        'resourcekey_input':resourcekey_input,

    }


    return render(request, 'hs_modflow/home.html', context)
