from django.db.models import Q 

from finance.models import SpentModel 

def update_recurring_spents(user, spents, spents_pks=None): 
    '''
        Recursive function to update all recurring spents 
    '''
    if spents is None: 
        return True 
    
    if spents_pks is None: 
        spents_pks = []

    for spent in spents:  
        spent.create_new_spent_for_recurring()
        spent.save()
            
        spents_pks.append(spent.pk)
        
        new_spent_obj = SpentModel.objects.filter(user=user, recurring=True).exclude(pk__in=spents_pks)
        
        if new_spent_obj.exists(): 
            return update_recurring_spents(user, spents=new_spent_obj, spents_pks=spents_pks)
        else: 
            return True 