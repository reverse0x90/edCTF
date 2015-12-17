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
              t.send('promptConfirmation', [
                'This will replace "' + live_ctf.get('name') + '" as the current online ctf.',
                'Are you sure?',
              ], function(confirmed){
                if(confirmed){
                  createCtf(name, true);
                } else {
                  t.set('modalErrorMessage', '');
                  t.set('modalErrorFields', {});
                }
              });
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
    promptConfirmation: function(messageArray, callback){
      this.set('modal.confirmMesg', messageArray);
      this.set('modal.confirmCallback', callback);
      this.set('modal.isConfirm', true);
    },
    openAdminCtfModal: function() {
      this.set('modal.isAdminCtf', true);
    },
    setSelectedCtf: function(ctf){
      this.set('errorMessage', '');
      this.set('errorFields', {});
      this.set('selectedCtf', ctf);
      this.set('selectedOption', {
        'view': true,
        'edit': false,
      });
    },
    setViewOption: function(){
      this.set('errorMessage', '');
      this.set('errorFields', {});
      this.set('selectedOption', {
        'view': true,
        'edit': false,
      });
    },
    setEditOption: function(){
      this.set('errorMessage', '');
      this.set('errorFields', {});
      this.set('editCtfName', this.get('selectedCtf.name'));
      this.set('editCtfLive', this.get('selectedCtf.live'));
      this.set('selectedOption', {
        'view': false,
        'edit': true,
      });
    },
    editCtf: function(){
      var t = this;
      var editCtfConfirmed = function(ctf, new_ctf){
        ctf.set('name', new_ctf.name);
        ctf.set('live', new_ctf.live);
        ctf.save().then(function(){
          // set option to view
          console.log('here');
          t.set('selectedOption', {
            'view': true,
            'edit': false,
          });
        }, function(err){
          ctf.rollbackAttributes();
          if (err.errors.message){
            t.set('errorMessage', err.errors.message);
            t.set('errorFields', err.errors.fields);
          } else {
            t.set('errorMessage', 'Server Error, unable to edit ctf');
            t.set('errorFields', {});
          }
        });
      };

      var name = this.get('editCtfName');
      var live = this.get('editCtfLive');
      var ctf = this.get('selectedCtf');
      if(live === ctf.get('live')){
        editCtfConfirmed(ctf, {
          'name': name,
          'live': live,
        });
      } else {
        var liveCtf = this.get('appController').get('ctf');
        if(liveCtf){
          if(liveCtf.get('live')){
            if(liveCtf.get('id') === ctf.get('id')){
              // liveCtf is going offline, confirm with user
              this.send('promptConfirmation', [
                'This will take the ctf "' + liveCtf.get('name') + '" offline.',
                'Are you sure?',
              ], function(confirmed){
                if(confirmed){
                  editCtfConfirmed(ctf, {
                    'name': name,
                    'live': live,
                  });
                }
              });
            } else {
              if(live){
                // replacing live ctf, confirm with user
                this.send('promptConfirmation', [
                  'This will replace "' + liveCtf.get('name') + '" as the current online ctf.',
                  'Are you sure?',
                ], function(confirmed){
                  if(confirmed){
                    editCtfConfirmed(ctf, {
                      'name': name,
                      'live': live,
                    });
                  }
                });
              } else {
                editCtfConfirmed(ctf, {
                  'name': name,
                  'live': live,
                });
              }
            }
          } else {
            // if liveCtf isnt live for some reason, just update the ctf
            editCtfConfirmed(ctf, {
              'name': name,
              'live': live,
            });
          }
        } else {
          editCtfConfirmed(ctf, {
            'name': name,
            'live': live,
          });
        }
      }
    },
    deleteCtf: function(){
      var t = this;
      var ctf = this.get('selectedCtf');

      this.send('promptConfirmation', [
        'This will DELETE the ctf "' + ctf.get('name') + '" and all challenges, scoreboards, and teams associated with it.',
        'Are you REALLY sure?!',
      ], function(confirmed){
        if(confirmed){
          // disallow live ctf deletion
          if(ctf.get('live')){
            t.set('errorMessage', 'Cannot delete a live ctf');
            t.set('errorFields', {});
          } else {
            // DELETE the ctf!
            ctf.deleteRecord();
            ctf.save().then(function(){
              // replace selected ctf with another
              var liveCtf = t.get('appController').get('ctf');
              if(liveCtf){
                t.set('selectedCtf', liveCtf);
              } else {
                var nextCtf = t.get('sortedCtfs');
                if(nextCtf){
                  nextCtf = nextCtf.get('firstObject');
                  if(nextCtf){
                    t.set('selectedCtf', nextCtf);
                  } else {
                    t.set('selectedCtf', undefined);
                  }
                } else {
                  t.set('selectedCtf', undefined);
                }
              }
              
              // set option to view
              t.set('selectedOption', {
                'view': true,
                'edit': false,
              });
            }, function(err){
              ctf.rollbackAttributes();
              if (err.errors.message){
                t.set('errorMessage', err.errors.message);
                t.set('errorFields', err.errors.fields);
              } else {
                t.set('errorMessage', 'Server Error, unable to delete ctf');
                t.set('errorFields', {});
              }
            });
          }
        } else {
          t.set('modalErrorMessage', '');
          t.set('modalErrorFields', {});
        }
      });
    },
  },
});
