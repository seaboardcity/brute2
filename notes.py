


Algorithm for picking cards

best_position_val = -100
best_positional_cpi_list = []
for all possible cpi (including counterattacks):
   if legal:
      determine the cpi position_val
      if position_val >= best_position_val:
         best_positional_cpi_list.append(cpi) #the cpi's themselves need to come back in the form ['a','0','b','0'] not 'a','0','b','0'
         best_position_val = position_val

best_cpi = []
best_hand_val = -100
for cpi in best_positional_cpi_list:
    determine cpi hand value
    if hand_val > best_hand_val:
        best_hand_val = hand_val
        best_cpi = cpi
    
         
      

