"""
Comparison between Sears, Rauch and Dawidowski tables of neutron scattering factors.
"""
from pathlib import Path

from periodictable import elements, nsf, nsf_tables
from periodictable.util import parse_uncertainty

def table_diffs():
    col = ['b_c', 'bp', 'bm', 'E', 'coh', 'inc', 'tot', 'abs']
    path = Path(__file__).parent / 'nsf_Dawidowski.txt'
    el = 0
    old_table = [line.split(',') for line in nsf.nsftable.split('\n')]
    index = 0
    with open(path, 'rb') as fd:
        for line in fd:
            line = line.decode('utf-8')
            if line[0] == '#':
                continue
            parts = line[:-1].split('\t')
            atom = parts[0]
            spin = parts[3]
            if atom[0] == ' ':
                if atom[-1] in 'abcdefghijklmnopqrstuvwxyz':
                    sym, z = atom[-2:], int(atom[1:-2])
                else:
                    sym, z = atom[-1:], int(atom[1:-1])
                assert int(parts[2]) == z, line
            else:
                sym = atom
                el = int(parts[1])
                z = int(parts[2]) if parts[2] else None
            code = f"{el}-{sym}" if z is None else f"{el}-{sym}-{z}"
            # Abundance is empty for mixed stable isotopes, 100 for
            # single stable isotope or half-life for unstable isotopes
            #abundance = float(parts[4]) if parts[4] else None
            while old_table[index][0] < code:
                print(f"<<< Missing {old_table[index][0]}")
                index += 1
            if old_table[index][0] == code:
                old = old_table[index][3:]
                index += 1
            else:
                old = ['']*len(col)
            new = parts[5:]
            if new[0].endswith('i'):
                b_re, b_im = new[0].split()
                new[0] = b_re
                # As stated in the paper the b_c.imag is computed from
                # the absorption cross section for 2200 m/s neutrons.
                # The following confirms this.
                #bpp = float(b_im.split('(')[0])
                #sigma_a = float(new[-1].split('(')[0])
                #print(code, "imag", bpp, -sigma_a/(2000*nsf.ABSORPTION_WAVELENGTH))
            def parse_value(v):
                if v.endswith('i'):
                    v = v.split()[0]
                v = v.replace(' ', '')
                if v.startswith('<'):
                    v = v[1:]
                if v.endswith('E') or v.endswith('*'):
                    v = v[:-1]
                return parse_uncertainty(v)
            #print(code, [parse_value(v) for v in old[:3]+old[4:]])
            #print(' '*len(code), [parse_value(v) for v in new[:3]+new[4:]])
            # New tables use E for estimated, and * for energy dependent
            # Many coherent cross sections (sigma_c, column 3) are assigned
            # zero when they were blank before.
            def no_tag(s):
                return s.replace('*','').replace('E','').replace('<','').replace(' ','')
            diff = [
                f"{c}: {x} => {y} " 
                for c, x, y in zip(col, old, new)
                if no_tag(x) != no_tag(y)
                and not (c == 'E' and no_tag(x) == '')
                and not (sym, z) in nsf_tables.ENERGY_DEPENDENT_TABLES
                #and c in ('b_c', 'tot', 'abs')
                and c in ('inc', 'tot', 'abs')
                ]
            if diff:
                print(code, '| '.join(diff))
            #print(code, parts[5:])


def sears_diffs():
    col = ['b_c', 'bp', 'bm', 'E', 'coh', 'inc', 'tot', 'abs']
    path = Path(__file__).parent / 'nsf_Sears.txt'
    el = 0
    old_table = [line.split(',') for line in nsf.nsftable.split('\n')]
    index = 0
    with open(path, 'rb') as fd:
        for line in fd:
            line = line.decode('utf-8')
            if line[0] == '#' or not line.strip():
                continue
            parts = line[:-1].split('\t')
            if not parts[0].strip() and not parts[2].strip():
                # Some lines contain only the imaginary partd of b_c and b_i.
                # Skip these for now.
                continue
            atom = parts[0].strip()
            spin = parts[3].strip()
            if atom:
                sym, el = atom, int(parts[1])
                z = int(parts[2].replace('*','')) if parts[2].strip() else None
            else:
                z = int(parts[2].replace('*',''))
            code = f"{el}-{sym}" if z is None else f"{el}-{sym}-{z}"
            # Abundance is empty for mixed stable isotopes, 100 for
            # single stable isotope or half-life for unstable isotopes
            #abundance = float(parts[4]) if parts[4] else None
            while old_table[index][0] < code:
                print(f"<<< Missing {old_table[index][0]}")
                index += 1
            if old_table[index][0] == code:
                old = old_table[index][3:]
                index += 1
            else:
                old = ['']*len(col)
            new = parts[5:]
            # New has bi instead of bp,bm and no E column
            new = parts[5:6] + ['']*3 + parts[7:]
            #print(code, new)
            def parse_value(v):
                if v.endswith('i'):
                    v = v.split()[0]
                v = v.replace(' ', '')
                if v.startswith('<'):
                    v = v[1:]
                if v.endswith('E') or v.endswith('*'):
                    v = v[:-1]
                return parse_uncertainty(v)
            #print(code, [parse_value(v) for v in old[:3]+old[4:]])
            #print(' '*len(code), [parse_value(v) for v in new[:3]+new[4:]])
            # New tables use E for estimated, and * for energy dependent
            # Many coherent cross sections (sigma_c, column 3) are assigned
            # zero when they were blank before.
            def no_tag(s):
                return s.strip().replace('*','').replace('E','').replace('<','').replace(' ','')
            diff = [
                f"{c}: {y} => {x} " 
                for c, x, y in zip(col, old, new)
                if 
                #no_tag(x) != no_tag(y)
                (c == 'E' or parse_value(x) != parse_value(y))
                # Only list values within 5%
                #and (c == 'E' or (parse_value(x)[0] and parse_value(y)[0] and abs((parse_value(x)[0]-parse_value(y)[0])/parse_value(x)[0]) > 0.03))
                and not (c == 'E' and no_tag(x) == '')
                and not (sym, z) in nsf_tables.ENERGY_DEPENDENT_TABLES
                #and c in ('b_c', 'tot', 'abs')
                and c in ('b_c', 'inc', 'tot', 'abs')
                ]
            if diff:
                print(code, '| '.join(diff))
                #print("  ", new); print("  ", old)
            #print(code, parts[5:])



if __name__ == "__main__":
    #table_diffs()
    sears_diffs()
