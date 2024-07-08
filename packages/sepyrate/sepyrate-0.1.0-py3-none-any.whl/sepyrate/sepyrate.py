
def digit_separation(amount, tsep, dsep=None):
    
    valint = int(str(amount).split('.')[0])
    temp = f'{valint:,}'
    
    if type(amount) == float:        
        valdec = str(amount).split('.')[1]
          
        if tsep == ',':
            if dsep is None or dsep == '.':
                return '.'.join([temp, valdec])
            else:
                raise ValueError("Unknown decimal separator for tsep=','!")
        
        elif tsep == '.':
            res = temp.replace(',', '.')
            if dsep is None or dsep == ',':                
                return ','.join([res, valdec])
            elif dsep == "'":
                return dsep.join([res, valdec])
            else:
                raise ValueError("Unkown decimal separator for tsep='.'!")
        
        elif tsep == ' ':
            res = temp.replace(',', ' ')
            if dsep is None or dsep == '.':                
                return '.'.join([res, valdec])
            elif dsep == ',':
                return dsep.join([res, valdec])
            else:
                raise ValueError("Unknown decimal separator for tsep=' '!")
        
        elif tsep == "'":
            res = temp.replace(",", "'")
            if dsep is None or dsep == '.':
                return '.'.join([res, valdec])
            elif dsep == ',':
                return dsep.join([res, valdec])
            else:
                msg = f"Unknown decimal separator dsep='{dsep}'"
                raise ValueError(msg)
                
            
    elif type(amount) == int:
        
        if tsep == ',':
            if dsep is None:
                return temp
            elif dsep == '.':
                res = f'{amount:,.2f}'
                return res.replace(',','*').replace('.', '.').replace('*',',')
            else:
                raise ValueError("Unknown decimal separator for tsep=','!")
                
            
        elif tsep == '.':
            if dsep is None:
                return temp.replace(',', '.')
            elif dsep == ',':
                res = f'{amount:,.2f}'
                return res.replace(',','*').replace('.', ',').replace('*','.')
            else:
                raise ValueError("Unkown decimal separator for tsep='.'!")
        
        elif tsep == ' ':
            if dsep is None:
                return temp.replace(',', ' ')
            elif dsep == '.':
                res = f'{amount:,.2f}'
                return res.replace(',','*').replace('.', '.').replace('*',' ')
            elif dsep == ',':
                res = f'{amount:,.2f}'
                return res.replace(',','*').replace('.', ',').replace('*',' ')
            else:
                raise ValueError("Unknown decimal separator for tsep=' '!")
                
        elif tsep == "'":
            if dsep is None:
                return temp.replace(",", "'")
            elif dsep == '.':
                res = f'{amount:,.2f}'
                return res.replace(',','*').replace('.', '.').replace('*', "'")
            elif dsep == ',':
                res = f'{amount:,.2f}'
                return res.replace(',','*').replace('.', ',').replace('*', "'")
            else:
                msg = f"Unknown decimal separator dsep='{dsep}'"
                raise ValueError(msg)
                
        else:
            raise ValueError("Unknown thousands separator!")
            
    else:
        raise ValueError("Cannot accept type other than int or float!")
                
