# -*- coding: utf-8 -*-
{
    'name': "sm_contributions",

    'summary': """
        Control people ofering money donations to the cooperative
    """,

    'description': """""",

    'author': "Som Mobilitat",
    'website': "https://www.sommobilitat.coop",

    'category': 'vertical-cooperative',
    'version': '12.0.0.0.7',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'vertical_carsharing'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/sm_account_journal.xml',
        'views/views.xml',
        'views/views_res_config_settings.xml',
        'views/views_contribution.xml',
        'views/views_contribution_line.xml',
        'views/views_contribution_interest.xml',
        'views/views_contribution_type.xml',
        'report/sm_contributions_report_line.xml',
        'report/sm_contributions_report.xml',
        'report/sm_contributions_contract.xml',
        'report/sm_contributions_contract_2.xml',
        'report/sm_contributions_contract_3.xml',
        'email_tmpl/contributions_contract.xml',
        'email_tmpl/contributions_contract_2.xml',
        'email_tmpl/contributions_contract_3.xml',
        'email_tmpl/contributions_year_line.xml',
        'wizards/wizards_sm_date_picker.xml',
        'wizards/wizards_sm_select_year_line.xml',

    ],
    # only loaded in demonstration mode
    'demo': [],
}
