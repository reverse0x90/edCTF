import Ember from 'ember';

export default Ember.Controller.extend({
  model: null,
  modal: {},
  appController: null,
  editCtfName: '',
  editCtfLive: false,
  errorMessage: '',
  errorFields: {},
  modalErrorMessage: '',
  modalErrorFields: {},
  ctfSorting: ['live:desc', 'id'],
  sortedCtfs: Ember.computed.sort('model', 'ctfSorting'),
  selectedCtf: null,
  selectedOption: {
    'view': true,
    'edit': false,
  },
  setSelectedCtf: function(){
    var live_ctf = this.get('appController').get('ctf');
    this.set('selectedCtf', live_ctf);
  }.observes('appController.ctf'),
  create: function(){
    var t = this;

    var createCtf = function(name, live){
      var ctf = t.store.createRecord('ctf', {
        name: name,
        live: live,
      });
      ctf.save().then(function(ctf){
        t.set('modal.isAdminCtf', false);
        t.set('modalErrorMessage', '');
        t.set('modalErrorFields', {});
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
          t.set('modalErrorMessage', err.errors.message);
          t.set('modalErrorFields', err.errors.fields);
        } else {
          t.set('modalErrorMessage', 'Server Error');
          t.set('modalErrorFields', {});
        }
      });
    };

    return function(name, live){
      // check if name is set
      if(!name){
        t.set('modalErrorMessage', 'Invalid CTF name');
        t.set('modalErrorFields', {'name': true});
        return;
      }

      // check if name already taken
      t.store.filter('ctf', function(ctf) {
        return ctf.get('name') === name;
      }).then(function(foundCtf) {
        var found = foundCtf.get('length');
        if(found){
          t.set('modalErrorMessage', 'CTF name already taken');
          t.set('modalErrorFields', {'name': true});
        } else {
          if(live){
            var live_ctf = t.get('appController.ctf');
            if(live_ctf){
              t.set('modal.confirmMesg', [
                'This will replace "' + live_ctf.get('name') + '" as the current online ctf.',
                'Are you sure?',
              ]);
              t.set('modal.confirmCallback', function(confirmed){
                if(confirmed){
                  createCtf(name, true);
                } else {
                  t.set('modalErrorMessage', '');
                  t.set('modalErrorFields', {});
                }
              });
              t.set('modal.isConfirm', true);
            } else {
              createCtf(name, true);
            }
          } else {
            createCtf(name, false);
          }
        }
      });
    };
  }.property('create'),
  actions: {
    openAdminCtfModal: function() {
      this.set('modal.isAdminCtf', true);
    },
    setSelectedCtf: function(ctf){
      this.set('selectedCtf', ctf);
      this.set('selectedOption', {
        'view': true,
        'edit': false,
      });
    },
    setViewOption: function(){
      this.set('selectedOption', {
        'view': true,
        'edit': false,
      });
    },
    setEditOption: function(){
      this.set('editCtfName', this.get('selectedCtf.name'));
      this.set('editCtfLive', this.get('selectedCtf.live'));
      this.set('selectedOption', {
        'view': false,
        'edit': true,
      });
    },
    editCtf: function(){
      var name = this.get('editCtfName');
      var live = this.get('editCtfLive');
      console.log('editing:', this.get('selectedCtf.id'), name, live);
      
      this.set('selectedOption', {
        'view': true,
        'edit': false,
      });
    },
    deleteCtf: function(){
      var name = this.get('selectedCtf.name');
      var live = this.get('selectedCtf.live');
      console.log('deleting:', this.get('selectedCtf.id'), name, live);

      // set selectCtf to proper ctf
      var liveCtf = this.get('appController').get('ctf');
      if(liveCtf){
        this.set('selectedCtf', liveCtf);
      } else {
        var nextCtfs = this.get('sortedCtfs');
        if(nextCtfs){
          var nextCtf = nextCtfs.get('firstObject');
          if(nextCtf){
            this.set('selectedCtf', nextCtf);
          } else {
            this.set('selectedCtf', undefined);
          }
        } else {
          this.set('selectedCtf', undefined);
        }
      }
      
      // set back to view
      this.set('selectedOption', {
        'view': true,
        'edit': false,
      });
    },
  },
});
