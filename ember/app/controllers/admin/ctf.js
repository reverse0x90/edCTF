import Ember from 'ember';

export default Ember.Controller.extend({
  model: null,
  modal: {},
  appController: null,
  errorMessage: '',
  errorFields: {},
  ctfSorting: ['live:desc', 'id'],
  sortedCtfs: Ember.computed.sort('model', 'ctfSorting'),
  create: null,
  setFunctions: function(){
    var t = this;

    var createCtf = function(name, live){
      var ctf = t.store.createRecord('ctf', {
        name: name,
        live: live,
      });
      ctf.save().then(function(ctf){
        t.set('modal.isAdminCtf', false);
        t.set('errorMessage', '');
        t.set('errorFields', {});
        if(ctf.get('live')){
          var live_ctf = t.get('appController.ctf');
          if(live_ctf){
            live_ctf.set('live', false);
          }
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

    var create = function(name, live){
      if(!name){
        t.set('errorMessage', 'Invalid CTF name');
        t.set('errorFields', {'name': true});
        return;
      }
      if(live){
        var live_ctf = t.get('appController.ctf');
        if(live_ctf){
          t.set('modal.confirmMesg', [
            'This will replace ' + live_ctf.get('name') + ' as the current online ctf.',
            'Are you sure?',
          ]);
          t.set('modal.confirmCallback', function(confirmed){
            if(confirmed){
              createCtf(name, true);
            } else {
              t.set('errorMessage', '');
              t.set('errorFields', {});
            }
          });
          t.set('modal.isConfirm', true);
        } else {
          createCtf(name, true);
        }
      } else {
        createCtf(name, false);
      }
    };
    this.set('create', create);
  }.observes('modal').on('init'),
  actions: {
    openAdminCtfModal: function() {
      this.set('modal.isAdminCtf', true);
    },
  },
});
