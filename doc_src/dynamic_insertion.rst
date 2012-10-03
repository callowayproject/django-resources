SUPPLYCLOSET_SETTINGS = {
    'SETUP_RESOURCES' = [
        'simpleapp.ModelA.related',
        'simpleapp.ModelA.see_also',
        'anotherapp.ModelB.related',
    ]
}

sets up REGISTRY:

{
    <simpleapp.ModelA>: ['related', 'see_also'],
    <anotherapp.ModelB>: ['related', ]
}