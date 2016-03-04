import Ember from 'ember';

export default Ember.Controller.extend({
  appController: null,
  isCreatingCategory: false,
  editingCategory: null,
  newCategoryName: '',
  errorMessage: '',
  ctfSorting: ['online:desc', 'id'],
  sortedCtfs: Ember.computed.sort('model', 'ctfSorting'),
  selectedCtf: null,
  setSelectedCtf: function(){
    var ctf = this.get('appController').get('ctf');
    if (ctf){
      this.set('selectedCtf', ctf);
    }
  }.observes('appController.ctf'),
  selectedChallengeboard: null,
  setSelectedChallengeboard: function(){
    var challengeboard = this.get('selectedCtf').get('challengeboard');
    if (challengeboard){
      this.set('selectedChallengeboard', challengeboard);
    }
  }.observes('selectedCtf'),
  setFocus: function(){
    setTimeout(function(){
      Ember.$('#inputCategory').focus();
    }, 200);
  }.observes('isCreatingCategory', 'editingCategory'),
  init: function(){
    Ember.$('#categoryDelete').click(function() {Ember.$('#categoryDelete').stop();});
  },
  actions: {
    promptConfirmation: function(messageArray, callback){
      this.set('modal.confirmMesg', messageArray);
      this.set('modal.confirmCallback', callback);
      this.set('modal.isConfirm', true);
    },
    changeSelectedCtf: function(ctf){
      this.set('selectedCtf', ctf);
    },
    openCreateCategory: function(){
      this.send('closeEditCategory');
      this.set('isCreatingCategory', true);
    },
    closeCreateCategory: function(){
      this.set('errorMessage', '');
      this.set('isCreatingCategory', false);
    },
    createCategory: function(){
      var challengeboard = this.get('selectedChallengeboard');
      var name = this.get('newCategoryName');
      var t =this;

      // error check here
      this.store.filter('category', function(category) {
        return category.get('name') === name;
      }).then(function(foundCategory) {
        var found = foundCategory.get('length');
        if(found){
          t.set('errorMessage', 'Category name already taken');
        } else {
          var category = t.store.createRecord('category', {
            challengeboard: challengeboard,
            name: name,
          });
          category.save().then(function(){
            t.send('closeCreateCategory');
            t.set('newCategoryName', '');
            t.set('errorMessage', '');
          }, function(err){
            category.rollbackAttributes();
            if (err.errors.message){
              t.set('errorMessage', err.errors.message);
            } else {
              t.set('errorMessage', 'Server error, unable to add category');
            }
          });
        }
      });
    },
    openEditCategory: function(category){
      var categoryCopy = {
        id: category.get('id'),
        name: category.get('name'),
      };
      this.send('closeCreateCategory');
      this.set('editingCategory', categoryCopy);
    },
    closeEditCategory: function(){
      this.set('errorMessage', '');
      this.set('editingCategory', null);
    },
    closeEditCategoryDelayed: function(){
      var t = this;
      setTimeout(function(){
        t.set('errorMessage', '');
        t.set('editingCategory', null);
      }, 200);
    },
    editCategory: function(){
      var t = this;
      var newCategory = this.get('editingCategory');
      var category = this.store.peekRecord('category', newCategory.id);

      if(category.get('name') === newCategory.name){
        this.send('closeEditCategory');
        this.set('errorMessage', '');
        return;
      }

      category.set('name', newCategory.name);
      category.save().then(function(){
        t.send('closeEditCategory');
        t.set('errorMessage', '');
      }, function(err){
        category.rollbackAttributes();
        if (err.errors.message){
          t.set('errorMessage', err.errors.message);
        } else {
          t.set('errorMessage', 'Server error, unable to edit category');
        }
      });
    },
    deleteCategory: function(category){
      var t = this;
      this.send('promptConfirmation', [
        'This will DELETE the category "' + category.get('name') + '" and all challenges associated with it.',
        'Are you sure?!',
      ], function(confirmed){
        if(confirmed){
          category.deleteRecord();
          category.save().then(function(){
            t.send('closeEditCategory');
            t.set('errorMessage', '');
          }, function(err){
            category.rollbackAttributes();
            if (err.errors.message){
              t.set('errorMessage', err.errors.message);
            } else {
              t.set('errorMessage', 'Server error, unable to delete category');
            }
          });
        }
      });
    },
    openCreateChallenge: function(category){
      this.set('modal.adminCategory', category);
      this.set('modal.adminChallenge', null);
      this.set('modal.isAdminChallenge', true);
    },
    closeChallenge: function(){
      this.set('modal.isAdminChallenge', false);
      this.set('modal.adminCategory', null);
      this.set('modal.adminChallenge', null);
      this.set('modal.errorMessage', '');
      this.set('modal.errorFields', {});
    },
    createChallenge: function(newChallenge){
      if(!newChallenge.title){
        this.set('modal.errorFields', {'title': true});
        this.set('modal.errorMessage', 'Invalid title');
        return;
      }

      var points = Number(newChallenge.points);
      if(!points){
        this.set('modal.errorFields', {'points': true});
        this.set('modal.errorMessage', 'Invalid points');
        return;
      }

      if(!newChallenge.description){
        this.set('modal.errorFields', {'description': true});
        this.set('modal.errorMessage', 'Invalid description');
        return;
      }

      if(!newChallenge.flag){
        this.set('modal.errorFields', {'flag': true});
        this.set('modal.errorMessage', 'Invalid flag');
        return;
      }

      var t = this;
      var challenge = t.store.createRecord('challenge', {
        category: newChallenge.category,
        title: newChallenge.title,
        points: points,
        description: newChallenge.description,
        flag: newChallenge.flag,
      });
      challenge.save().then(function(){
        t.send('closeChallenge');
      }, function(err){
        challenge.rollbackAttributes();
        if (err.errors.message){
          t.set('modal.errorMessage', err.errors.message);
        } else {
          t.set('modal.errorMessage', 'Server error, unable to add challenge');
        }
      });
    },
    openEditChallenge: function(challenge){
      this.set('modal.adminCategory', null);
      this.set('modal.adminChallenge', challenge);
      this.set('modal.isAdminChallenge', true);
    },
    editChallenge: function(challenge){
      if(!challenge.get('title')){
        this.set('modal.errorFields', {'title': true});
        this.set('modal.errorMessage', 'Invalid title');
        return;
      }

      var points = Number(challenge.get('points'));
      if(!points){
        this.set('modal.errorFields', {'points': true});
        this.set('modal.errorMessage', 'Invalid points');
        return;
      }

      if(!challenge.get('description')){
        this.set('modal.errorFields', {'description': true});
        this.set('modal.errorMessage', 'Invalid description');
        return;
      }

      if(!challenge.get('flag')){
        this.set('modal.errorFields', {'flag': true});
        this.set('modal.errorMessage', 'Invalid flag');
        return;
      }

      var t = this;
      challenge.save().then(function(){
        t.send('closeChallenge');
      }, function(err){
        challenge.rollbackAttributes();
        if (err.errors.message){
          t.set('modal.errorMessage', err.errors.message);
        } else {
          t.set('modal.errorMessage', 'Server error, unable to edit challenge');
        }
      });
    },
    deleteChallenge: function(challenge){
      var t = this;
      challenge.deleteRecord();
      challenge.save().then(function(){
        t.send('closeChallenge');
      }, function(err){
        challenge.rollbackAttributes();
        if (err.errors.message){
          t.set('modal.errorMessage', err.errors.message);
        } else {
          t.set('modal.errorMessage', 'Server error, unable to delete challenge');
        }
      });
    },
  },
});
