import Ember from 'ember';

export default Ember.Controller.extend({
  modal: {},
  appController: null,
  errorMessage: '',
  errorFields: {},
  create: null,
  setFunctions: function(){
    var t = this;

    var create = function(formName, formLive){
      if(!formName){
        t.set('errorMessage', 'Invalid CTF name');
        t.set('errorFields', {'name': true});
        return;
      }
      var name = formName;
      var live = false;
      if(formLive){
        live = true;
      }

      var ctf = t.store.createRecord('ctf', {
        name: name,
        live: live,
      });

      ctf.save().then(function(ctf){
        t.set('modal.isAdminCtf', false);
        t.set('errorMessage', '');
        t.set('errorFields', {});
        if(ctf.get('live')){
          t.set('appController.ctf', ctf);
        }
      }, function(err){
        ctf.deleteRecord();
        if (err.errors.message){
          t.set('errorMessage', err.errors.message);
          t.set('errorFields', err.errors.fields);
        } else {
          t.set('errorMessage', 'Server Error');
          t.set('errorFields', {});
        }
      });
    };
    this.set('create', create);
  }.observes('modal').on('init'),
  actions: {
    openAdminCtfModal: function() {
      this.set('modal.isAdminCtf', true);
    },
  },
});
