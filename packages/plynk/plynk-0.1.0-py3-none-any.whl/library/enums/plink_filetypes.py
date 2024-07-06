from enum import StrEnum


class PlinkFileType(StrEnum):
    BED = "bed"  # Binary PED file
    BIM = "bim"  # Binary map file
    EIGENVAL = "eigenval"  # Eigenvalues from PCA
    EIGENVEC = "eigenvec"  # Eigenvectors from PCA
    FAM = "fam"  # Family information file
    HET = "het"  # Heterozygosity report
    LOG = "log"  # Log file
    NOSEX = "nosex"  # No sex determination report
    MAP = "map"  # Map file
    PED = "ped"  # PED file (pedigree and genotype information)
    HWE = "hwe"  # Hardy-Weinberg equilibrium test output
    FREQ = "freq"  # Allele frequency data
    ASSOC = "assoc"  # Association test output
    MISSING = "missing"  # Missing genotype report
    HOMOZYG = "homozyg"  # Runs of homozygosity data
    CLST = "clst"  # Cluster assignments from population stratification
    PHENO = "pheno"  # Phenotype data
    QFAM = "qfam"  # Quantitative trait data for family-based association tests
    GENO = "geno"  # Genotype counts for each SNP
    LGEN = "lgen"  # Linkage format genotype data
