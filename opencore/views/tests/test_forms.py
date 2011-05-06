from colander import (
    MappingSchema,
    SchemaNode,
    String,
    )
from deform.widget import (
    CheckboxWidget,
    Widget,
    )
from mock import Mock
from opencore.views.api import get_template_api
from opencore.views.forms import (
    BaseController,
    KarlUserWidget,
    TOUWidget,
    )
from repoze.bfg import testing
from testfixtures import (
    Replacer,
    ShouldRaise,
    Comparison as C,
    )
from unittest import TestCase
from webob.exc import HTTPFound

class TestBaseController(TestCase):

    def setUp(self):
        self.context = testing.DummyModel()
        self.request = testing.DummyRequest()
        self.request.api = get_template_api(self.context, self.request)
        self.controller = BaseController(self.context,self.request)
        # a simple schema to test
        class Schema(MappingSchema):
            field = SchemaNode(String())
        self.controller.Schema = Schema
        # stub out the handle_submit method with mock
        self.controller.handle_submit = Mock()

    def test_api(self):
        self.assertTrue(self.controller.api is self.request.api)

    def test_data(self):
        self.assertEqual(
            self.controller.data,
            dict(api=self.request.api)
            )

    def test_call_get(self):
        result = self.controller()
        self.assertTrue(result is self.controller.data)
        self.assertTrue(result['form'].startswith('<form id="deform"'))
        self.assertFalse(self.controller.handle_submit.called)

    def test_call_cancel(self):
        self.request.POST['cancel']='cancel'
        result = self.controller()
        self.assertTrue(isinstance(result,HTTPFound))
        self.assertEqual(result.location,'http://example.com/')
        self.assertFalse(self.controller.handle_submit.called)

    def test_call_save_validation_failed(self):
        self.request.POST['save']='save'
        result = self.controller()
        self.assertTrue(result is self.controller.data)
        self.assertTrue(result['form'].startswith('<form id="deform"'))
        self.assertTrue('Errors have been highlighted' in result['form'])
        self.assertFalse(self.controller.handle_submit.called)
        
    def test_call_save_okay(self):
        self.request.POST['save']='save'
        self.request.POST['field']='something'
        result = self.controller()
        self.assertTrue(
            result is self.controller.handle_submit.return_value
            )
        self.assertTrue(self.controller.handle_submit.called)

    def test_different_buttons(self):
        with Replacer() as r:
            self.controller.buttons = ('one','two')
            Form = Mock()            
            r.replace('opencore.views.forms.Form',Form)

            self.controller()

            Form.assert_called_with(
                C(SchemaNode),
                buttons = ('one','two'),
                )
            
    def test_call_save_different_buttons(self):
        # check that we use the last button provided
        # as the trigger to process the submit
        self.controller.buttons = ('one','two')
        self.request.POST['two']='two'
        result = self.controller()
        self.assertTrue(result is self.controller.data)
        self.assertTrue(result['form'].startswith('<form id="deform"'))
        self.assertTrue('Errors have been highlighted' in result['form'])
        self.assertFalse(self.controller.handle_submit.called)
        
class TestKarlUserWidget(TestCase):

    def setUp(self):
        self.field = Mock()
        self.field.name='users'
        self.widget = KarlUserWidget()

    def test_subclass(self):
        # assume other bits behave as per base widget :-)
        self.assertTrue(isinstance(self.widget,Widget))
                        
    def test_serialize(self):
        # call
        self.assertEqual(
            self.widget.serialize(self.field,''),
            self.field.renderer.return_value
            )
        # check we called renderer correctly
        self.field.renderer.assert_called_with(
            'karluserwidget',
            cstruct=(),
            field=self.field
            )

    def test_serialize_field_not_users(self):
        self.field.name = 'somethingelse'
        
        with ShouldRaise(Exception(
                "This widget must be used on a field named 'users'"
                )):
            self.widget.serialize(self.field,''),

        # check renderer not called
        self.assertFalse(self.field.renderer.called)

    def test_deserialize(self):
        pstruct = []

        returned = self.widget.deserialize(self.field,pstruct)

        # use identity to check we just pass through
        self.assertTrue(returned is pstruct)

class TestTOUWidget(TestCase):

    def setUp(self):
        self.field = Mock()
        self.field.name='terms_of_use'
        self.widget = TOUWidget()

    def test_subclass(self):
        # assume other bits behave as per base widget :-)
        self.assertTrue(isinstance(self.widget,CheckboxWidget))

    def test_template(self):
        self.assertEqual(self.widget.template,'terms_of_use')
