

def write_output(out:list):
    with open('output.txt', 'w') as f:
        for line in out:
            f.write(line+'\n')
         
def return_all_prod_list(obj_k, obj_dependencies):
    prod_pipeline = []
    t_tot = 0
    
    for o in obj_dependencies[obj_k]['id_depend']:
        if obj_dependencies[o]['n_depend'] == 0:
            prod_pipeline =  prod_pipeline + [o] 
            t_tot = t_tot + obj_dependencies[o]['t_prod']

        else:
            prod_pipeline_1, t_tot_1 = return_all_prod_list(o, obj_dependencies)
            prod_pipeline = prod_pipeline_1 + prod_pipeline
            t_tot += t_tot_1
            
    prod_pipeline =  prod_pipeline + [obj_k]
    t_tot = t_tot + obj_dependencies[obj_k]['t_prod']

    return prod_pipeline, t_tot
            
if __name__ == '__main__':
    with open('input-Finale/input') as f:
        lines = f.readlines()
    
    header = lines[0].split()
    tot_obj = int(header[0])
    tot_final_obj = int(header[1])
    tot_assembly_chain = int(header[2])
    

    obj_dependencies = {
        x.split()[0] : {
        't_prod':int(x.split()[1]),
        't_trasp':int(x.split()[2]),
        'n_depend':int(x.split()[3]),
        'id_depend':x.split()[4:]
    }  for x in lines[1:tot_obj+1]}
    
    
    final_obj_info = {
        x.split()[0]:{
        't_max_prod': int(x.split()[1]),
        'value': int(x.split()[2])
    } for x in lines[tot_obj+1:]}
    
    final_obj_info_sorted = dict(sorted(final_obj_info.items(), key=lambda x:x[1]['t_max_prod']) )
    

    assembly_chain_dict= {
        c+1:{
        'time_last_prod': 0,
        'actual_obj': None,
        'objs_on_chain':[]}
        for c in range(tot_assembly_chain) 
    }
    
    
    total_production_pipeline =[]
    i = 0
    for obj_k, obj_v in final_obj_info_sorted.items():
        i+=1
        production_list, total_prod_time = return_all_prod_list(obj_k, obj_dependencies) # si parte da quelli con 0 oggetti fino a quelli con piú oggetti, con dipendenze controllare in fila
        
        pnts = 0
        best_pnts = 0
        best_chain = None
        for chain, v_chain in assembly_chain_dict.items():
            pnts = obj_v['value'] + (obj_v['t_max_prod'] - (v_chain['time_last_prod'] + total_prod_time + (6-chain)*obj_dependencies[obj_k]['t_trasp']))
            
            
            if best_chain == None:
                best_chain = chain
                best_pnts = pnts
            else:
                if pnts > best_pnts:
                    best_chain = chain
                    best_pnts = pnts
                
        assembly_chain_dict[best_chain]['time_last_prod'] += total_prod_time
        
        
        for obj in production_list:
            total_production_pipeline.append(f"{obj} {best_chain}") #{obj_dependencies[obj]['n_depend']} {obj_dependencies[obj]['id_depend']}")
        if i == 1: break        
            

    
    write_output(total_production_pipeline)
        