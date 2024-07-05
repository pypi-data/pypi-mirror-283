import cobra, pandas as pd, importlib_resources, numpy as np
from pyensembl import EnsemblRelease

class FBA:
    def __init__(self):
        self.model_genes=[]
        my_resources = importlib_resources.files("humangemlib")
        data = my_resources.joinpath("Human-GEM.xml").read_text()
        self.model=cobra.io.read_sbml_model(data)
        self.ensembl_data = EnsemblRelease(release=111, species='homo_sapiens')
        self.gene_ensembl_table = dict()      # gene_ensemble_table['CDA2F'] = 'ENSG00000012861'
        self.model_genetype=dict()
        self.pure_genes=[]
        self.ko_candidate_genes=[]
        
        # FUTURE DIRECTIONS FOR FBA
        self.linc_genes=[]
        self.dash_genes=[]
        self.comma_genes=[]

        for i in self.model.genes:
            try:
                self.model_genes.append(self.ensembl_data.gene_by_id(i.id).gene_name)
                self.gene_ensembl_table[self.ensembl_data.gene_by_id(i.id).gene_name]=i.id
                self.model_genetype[self.ensembl_data.gene_by_id(i.id).gene_name]=self.ensembl_data.gene_by_id(i.id).biotype
            except ValueError:
                pass

    def gene_type_separation(self, geneList=None):
        if geneList == None:
            my_resources = importlib_resources.files("humangemlib")
            df = my_resources.joinpath('cleaneddata.tsv')
            df=pd.read_csv(df, sep='\t')
            geneList=list(df.mappedGenes)
        self.gwas_genes=set(geneList)
        op=[]
        for i in self.gwas_genes:
            if type(i) is str:
                op.append(i)
        self.gwas_genes=op
        for i in self.gwas_genes:
            if '-' in i:
                if 'LINC' in i:
                    self.linc_genes.append(i)
                else:
                    ds=[]
                    for j in i.split('-'):
                        if j[0]!=' ':
                            ds.append(j)
                        else:
                            ds.append(j[1:])
                    self.dash_genes.append(ds)
            elif ',' in i:
                p=[]
                for j in i.split(','):
                    p.append(j)
                self.comma_genes.append(p)
            else:
                self.pure_genes.append(i)
        for i in self.pure_genes:
            if i in self.model_genes:
                self.ko_candidate_genes.append(i)
    
    def solution_to_dict(self, solution, ko_gene='None'):
        solution_dict={
            
            'knockout_gene': ko_gene,
            'objective_value':solution.objective_value,
        }
        solution_dict.update(solution.fluxes.to_dict())
        return solution_dict

    
    def knockout_fluxes_dict(self, objective=None, ko_genes=[]):
        if len(ko_genes) == 0:
            ko_genes = self.ko_candidate_genes
        solutions=[self.solution_to_dict(self.model.optimize())]
        for i in ko_genes:
            with self.model:
                self.model.genes.get_by_id(self.gene_ensembl_table[i]).knock_out()
                solutions.append(self.solution_to_dict(self.model.optimize(),ko_gene=i))
        return solutions
    
    def knockout_fluxes(self, objective=None, ko_genes=[]):
        return pd.DataFrame(self.knockout_fluxes_dict(objective, ko_genes))

    # don't use, takes too much time. needs reworking
    def knockout_flux_ranges(self, ko_genes=[]):
        if len(ko_genes) == 0:
            ko_genes = self.ko_candidate_genes
        solutions=[cobra.flux_analysis.flux_variability_analysis(self.model)]
        model_genes=dict()
        for i in self.model.genes:
            model_genes[i.id]=i
        for i in ko_genes:
            self.model.genes.get_by_id(self.gene_ensembl_table[i]).knock_out()
            solutions.append(cobra.flux_analysis.flux_variability_analysis(self.model))
            self.model.genes.get_by_id(self.gene_ensembl_table[i]).functional=True
        return solutions

    def flux_differentials(self, solutions):
        flux_diff=[]
        for i in range(len(self.ko_candidate_genes)):
            t={
                'knockout_gene':self.ko_candidate_genes[i] 
            }
            k=pd.Series(pd.Series(solutions.iloc[0][1:])-pd.Series(solutions.iloc[i+1][1:]))
            t.update(k.to_dict())
            flux_diff.append(t)
        return flux_diff
    
    def unique_fluxes(self, solutions):
        unique_fluxes=[{'num':1, 'fluxes':pd.Series(solutions.iloc[0,2:]), 'knockout_genes':['None']}]
        for i in range(1,len(solutions)-1):
            unique=True
            for j in unique_fluxes:
                if np.allclose(np.array(j['fluxes'].values, dtype=float),np.array(pd.Series(solutions.iloc[i,2:].values), dtype=float)) and solutions.iloc[i,:]['knockout_gene']!='None':
                    unique=False
                    j['num']+=1
                    j['knockout_genes'].append(solutions.iloc[i,:]['knockout_gene'])
                    break
            if unique:
                unique_fluxes.append({'num':1, 'fluxes':pd.Series(solutions.iloc[i,2:]), 'knockout_genes':[solutions.iloc[i,:]['knockout_gene']]})
        u=[]
        for i in unique_fluxes:
            t={'num':i['num'], 'knockout_genes':i['knockout_genes']}
            t.update(i['fluxes'].to_dict())
            u.append(t)
        return u
    
    # can be reworked to use list of series for solutions in means. currently unindexed in reactions and genes. good for specific use case but lazy programming.
    def mean_solutions(self, n=5, knockouts=114, reactions=12997):
        sols=[]
        diffs=[]
        for i in range(n):
            self.__init__()
            self.gene_type_separation()
            t=pd.DataFrame(self.knockout_fluxes())
            sols.append(t)
            diffs.append(pd.DataFrame(self.flux_differentials(t)))
        t=np.array(sols)
        means=np.empty(shape=(knockouts,reactions))
        stddevs=np.empty(shape=(knockouts,reactions))
        for i in range(knockouts):
            for j in range(reactions):
                p=[]
                for k in range(len(t)):
                    if not type(t[k][i][j]) is str:
                        p.append(t[k][i][j])
                if len(p)!=0:
                    means[i][j]=np.mean(p)
                    stddevs[i][j]=np.std(p)
        return {
        'mean_solutions':means,
        'std_dev':stddevs
        }