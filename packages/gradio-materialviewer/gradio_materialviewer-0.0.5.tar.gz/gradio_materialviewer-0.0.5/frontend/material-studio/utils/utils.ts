import { VESTA_COLOR_TABLE } from 'dpmol';
import { ElementSymbolColors } from 'dpmol';
import { Color } from 'dpmol';
import { StructureElement, StructureProperties } from 'dpmol';
import { Loci } from 'dpmol';
import { MoleculeInfoParam } from 'dpmol';
import { Lattice, Atom, AtomParams, LatticeParams, MaterialItem, ASEDataItem, MaterialCleaveParams } from '../model';
import { Bulk } from './bulk';
import { cellparToCell } from './cell';
import { Matrix, add, det, identity, inv, mod, multiply } from 'mathjs';
// import { getExtByName } from '@@shared/model/workspace/node/util';
import { buildBulk, getSurfaceVector } from './surface-cleavage';

const Tolerance = 0.005;

export const MaterialExts = ['cif', 'dump', 'xyz', 'POSCAR'];

function combineElements(arr: number[], num = arr.length, combine = [] as number[][]): number[][] {
    if (num === 0) return [];
    if (num === 1) return [...combine, ...arr.map(n => [n])];
    if (arr.length === num) return combineElements(arr, num - 1, [arr.slice()]);
    for (let i = 0; i < arr.length - 1; i++) {
        for (let j = i + 1; j < arr.length; j++) {
            combine.push([arr[i], arr[j]]);
        }
    }
    return combineElements(arr, num - 1, combine);
}

export function isSameVec(source: number[], target: number[]) {
    return source.every((n, i) => n === target[i]);
}

export function isOriginVec(image: number[]) {
    return isSameVec(image, [0, 0, 0]);
}

export function isMaterialFilename(name: string) {
    const ext = 'abc';
    return MaterialExts.includes(ext);
}

export function createOriginalMaterial(params: { lattice?: LatticeParams; atoms: AtomParams[] }): MaterialItem {
    const material: MaterialItem = {
        expand: [1, 1, 1],
        atoms: [],
        lattice: undefined,
    };
    const lattice = params?.lattice ? createLatticeByParams(params?.lattice) : undefined;
    const atoms = params.atoms.map((a, index) => {
        const atom = createAtom(a, {
            lattice,
            order: index,
        });

        return atom;
    });

    material.lattice = lattice;
    material.atoms = atoms;
    return material;
}

export function createSymmetryMaterial(material: MaterialItem): MaterialItem {
    if (!material.lattice) {
        return material;
    }
    const symmetryMaterial = createOriginalMaterial({
        lattice: material.lattice,
        atoms: material.atoms,
    });
    const { atoms } = symmetryMaterial;
    const symmetryAtoms = getSymmetryAtoms(atoms, material.lattice);

    symmetryMaterial.atoms = [...symmetryMaterial.atoms, ...symmetryAtoms];

    return symmetryMaterial;
}

export function getParamsFromSymmetryMaterial(material: MaterialItem): MoleculeInfoParam {
    const elements: string[] = [];
    const xyzs: number[][] = [];

    material.atoms.map(atom => {
        elements.push(atom.element);
        xyzs.push(atom.xyz);
    });

    return {
        elements,
        xyzs,
        lattice: material.lattice,
    };
}

export function getTransMatrix4FormSymmetryVec(symmetryVec: number[], matrix: number[][]) {
    // const { matrix } = lattice
    let transVec3 = [0, 0, 0];
    symmetryVec.forEach((symmetry, idx) => {
        if (!symmetry) {
            return;
        }
        transVec3 = add(transVec3, multiply(matrix[idx], symmetry)) as number[];
    });
    const transMatrix4 = (identity(4) as Matrix).toArray() as number[][];
    transVec3.forEach((n, idx) => {
        transMatrix4[3][idx] = n;
    });
    return transMatrix4;
}

export function transformMatrix4(vec: number[], matrix4: number[][]) {
    const [x, y, z] = vec;
    const w = 1 / (matrix4[0][3] * x + matrix4[1][3] * y + matrix4[2][3] * z + matrix4[3][3] || 1.0);
    const a = (matrix4[0][0] * x + matrix4[1][0] * y + matrix4[2][0] * z + matrix4[3][0]) * w;
    const b = (matrix4[0][1] * x + matrix4[1][1] * y + matrix4[2][1] * z + matrix4[3][1]) * w;
    const c = (matrix4[0][2] * x + matrix4[1][2] * y + matrix4[2][2] * z + matrix4[3][2]) * w;
    return [a, b, c];
}

export function createLatticeByParams(params: LatticeParams): Lattice {
    const { a, b, c, alpha, beta, gamma, spacegroup } = params;
    const matrix = params.matrix || cellparToCell([a, b, c, alpha, beta, gamma]);
    const invertMatrix = inv(matrix);

    const vecA = matrix[0];
    const vecB = matrix[1];
    const vecC = matrix[2];

    const volume = det(matrix);

    return {
        spacegroup,
        a,
        b,
        c,
        volume,
        alpha,
        beta,
        gamma,
        vecA,
        vecB,
        vecC,
        matrix,
        invertMatrix,
    };
}

export function createAtom(
    params: AtomParams,
    extraParams?: {
        order?: number;
        lattice?: Lattice;
        symmetry?: number[];
    }
): Atom {
    const { element } = params;
    const { order, lattice, symmetry } = extraParams || {};

    if (!params.abc && !params.xyz) {
        throw new Error('createAtom: Need xyz or abc!');
    }

    if (!lattice && !params.xyz) {
        throw new Error('createAtom: Need xyz or lattice!');
    }

    let abc = (() => {
        const { xyz, abc } = params;
        // case1: 非晶体，无abc，无lattice
        if (!lattice) {
            return undefined;
        }

        // case2: 晶体，非对称性，已有xyz，计算abc
        if (!abc) {
            return multiply(xyz!, lattice.invertMatrix) as number[];
        }

        // case3: 晶体，非对称性，已有abc
        if (!symmetry || isOriginVec(symmetry)) {
            return abc;
        }

        // case4: 晶体，有对称性，已有abc，计算对称位置的abc
        const transMatrix4 = getTransMatrix4FormSymmetryVec(symmetry, (identity(3) as Matrix).toArray() as number[][]);
        const symmetryAbc = transformMatrix4(abc, transMatrix4);
        return symmetryAbc;
    })();

    let xyz = (() => {
        const { xyz, abc } = params;
        // case1: 非晶体，无lattice
        if (!lattice) {
            return xyz!;
        }

        // case2: 晶体，非对称性，已有abc，计算xyz
        if (!xyz) {
            return multiply(abc!, lattice.matrix) as number[];
        }

        // case3: 晶体，非对称性，已有xyz
        if (!symmetry || isOriginVec(symmetry)) {
            return xyz;
        }

        // case4: 晶体，有对称性，已有xyz，计算对称位置的xyz
        const transMatrix4 = getTransMatrix4FormSymmetryVec(symmetry, lattice.matrix);
        const symmetryXyz = transformMatrix4(xyz, transMatrix4);
        return symmetryXyz;
    })();

    // 超出晶格坐标，处理回晶格内
    const needRecalculate = abc && abc.some(n => n < 0 || n > 1);
    if (needRecalculate) {
        abc = mod(abc!, 1);
        xyz = multiply(abc!, lattice!.matrix) as number[];
    }

    return {
        element,
        xyz,
        abc,
        order,
        symmetry,
    };
}

export function getSymmetryAtoms(atoms: Atom[], lattice: Lattice) {
    const symmetryAtoms: Atom[] = [];

    atoms.forEach((atom, idx) => {
        const { abc } = atom;
        if (!abc || abc[0] === undefined) return;

        {
            const zeroElements = [];
            if (Math.abs(abc[0]) <= Tolerance) zeroElements.push(0);
            if (Math.abs(abc[1]) <= Tolerance) zeroElements.push(1);
            if (Math.abs(abc[2]) <= Tolerance) zeroElements.push(2);
            const coordPermutations = combineElements(zeroElements);
            const perms = coordPermutations.map(elements => [
                Number(elements.includes(0)),
                Number(elements.includes(1)),
                Number(elements.includes(2)),
            ]);
            perms.forEach(perm => {
                const sAtom = createAtom(atom, {
                    order: idx,
                    lattice,
                    symmetry: perm,
                });
                symmetryAtoms.push(sAtom);
            });
        }

        {
            const oneElements = [];
            if (Math.abs(1 - abc[0]) <= Tolerance) oneElements.push(0);
            if (Math.abs(1 - abc[1]) <= Tolerance) oneElements.push(1);
            if (Math.abs(1 - abc[2]) <= Tolerance) oneElements.push(2);
            const coordPermutations = combineElements(oneElements);
            const perms = coordPermutations.map(elements => [
                -Number(elements.includes(0)),
                -Number(elements.includes(1)),
                -Number(elements.includes(2)),
            ]);
            perms.forEach(perm => {
                const sAtom = createAtom(atom, {
                    order: idx,
                    lattice,
                    symmetry: perm,
                });
                symmetryAtoms.push(sAtom);
            });
        }
    });

    return symmetryAtoms;
}

export function getElementLociInfo(loci: Loci) {
    if (loci.kind !== 'element-loci') {
        return;
    }
    const stats = StructureElement.Stats.ofLoci(loci);
    const location = stats.elementCount ? stats.firstElementLoc : stats.firstStructureLoc;
    const x = StructureProperties.atom.x(location);
    const y = StructureProperties.atom.y(location);
    const z = StructureProperties.atom.z(location);
    // const sourceIndex = StructureProperties.atom.sourceIndex(location)
    const type_symbol = StructureProperties.atom
        .type_symbol(location)
        .split('')
        .map((s, i) => (i === 0 ? s : s.toLowerCase()))
        .join('');

    return {
        index: location.element,
        element: type_symbol,
        // color: getElementColor(type_symbol),
        x,
        y,
        z,
    };
}

export function getCleavageSurf(params: MaterialCleaveParams, origin: MaterialItem) {
    const { lattice } = origin;
    if (!lattice) {
        return;
    }
    const { matrix } = lattice;
    const { h, k, l, depth } = params;
    const [coefficient, cellVec] = getSurfaceVector(
        matrix[0] as [number, number, number],
        matrix[1] as [number, number, number],
        matrix[2] as [number, number, number],
        h,
        k,
        l
    );
    const bulk = material2Bulk(origin)!;
    const surf = buildBulk(bulk, coefficient, depth, true);

    return surf;
}

export function bulk2Material(bulk: Bulk) {
    const material: MaterialItem = {
        expand: [1, 1, 1],
        atoms: [],
        lattice: undefined,
    };
    const cell = bulk.getCell();
    let lattice: Lattice | undefined = undefined;

    if (cell) {
        lattice = createLatticeByParams({
            spacegroup: {
                symbol: 'P 1',
                no: 1,
            },
            matrix: cell,
            a: 0,
            b: 0,
            c: 0,
            alpha: 0,
            beta: 0,
            gamma: 0,
        });
    }

    const symbols = bulk.getSymbols();
    const xyzs = bulk.getCoordinates();
    const abcs = bulk.getFractionalCoordinates() as number[][];
    const atoms = symbols.map((element, index) => {
        const atom = createAtom(
            {
                element,
                xyz: xyzs[index],
                abc: abcs[index],
            },
            {
                lattice,
                order: index,
            }
        );
        return atom;
    });

    material.lattice = lattice;
    material.atoms = atoms;
    return material;
}

export function material2Bulk(material: MaterialItem) {
    const { lattice, atoms } = material;
    if (!lattice) {
        return;
    }
    const cell = [lattice.vecA, lattice.vecB, lattice.vecC];
    const symbols: string[] = [];
    const position: number[][] = [];
    const fracPosition: number[][] = [];
    atoms.forEach(atom => {
        symbols.push(atom.element);
        position.push(atom.xyz);
        fracPosition.push(atom.abc!);
    });
    const bulk = new Bulk(cell, symbols, position, fracPosition);
    return bulk;
}

export function getElementColor(element: string, biology = false) {
    if (biology) {
        return `#${{ ...ElementSymbolColors, C: 0x48e533 }[
            element.toUpperCase() as keyof typeof ElementSymbolColors
        ].toString(16)}`;
    }

    const color = (VESTA_COLOR_TABLE as { [key: string]: number })[element.toUpperCase()];
    const rgb = Color.toRgb(Color(color));
    return `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`;
}

export function getVertexByVectors(vectors: number[][]) {
    const a = vectors[0];
    const b = vectors[1];
    const c = vectors[2];
    const p0 = [0, 0, 0];
    const p1 = a;
    const p2 = b;
    const p3 = add(a, b);
    const p4 = c;
    const p5 = add(a, c);
    const p6 = add(b, c);
    const p7 = add(add(a, b), c);

    return [p0, p1, p2, p3, p4, p5, p6, p7];
}

export function getPointsByVertex(vertex: number[][]) {
    const [p0, p1, p2, p3, p4, p5, p6, p7] = vertex;

    return [
        [p0, p1],
        [p0, p2],
        [p1, p3],
        [p2, p3],
        [p0, p4],
        [p1, p5],
        [p2, p6],
        [p3, p7],
        [p4, p5],
        [p4, p6],
        [p5, p7],
        [p6, p7],
    ];
}

export function ase2Material(ase: ASEDataItem): MaterialItem {
    const { length, angle, spacegroup: aseSpacegroup, atoms: aseAtoms } = ase;
    const material: MaterialItem = {
        expand: [1, 1, 1],
        atoms: [],
        lattice: undefined,
    };

    const lattice = (() => {
        if (!length || !angle || !aseSpacegroup) {
            return;
        }
        const [a, b, c] = length;
        const [alpha, beta, gamma] = angle;
        const spacegroup = {
            symbol: aseSpacegroup[1],
            no: aseSpacegroup[0],
        };
        const lattice = createLatticeByParams({
            spacegroup,
            a,
            b,
            c,
            alpha,
            beta,
            gamma,
        });
        return lattice;
    })();

    const atoms = aseAtoms.map((item, index) => {
        const params = {
            element: item.formula,
            xyz: item.cart_coord,
            abc: item.frac_coord,
        };
        const atom = createAtom(params, {
            lattice,
            order: index,
        });

        return atom;
    });

    material.lattice = lattice;
    material.atoms = atoms;
    return material;
}

export function material2Ase(material: MaterialItem) {
    const { atoms: matAtoms, lattice } = material;
    const ase: ASEDataItem = {
        atoms: [],
    };
    matAtoms.forEach(item => {
        ase.atoms.push({
            cart_coord: item.xyz,
            formula: item.element,
            frac_coord: item.abc!,
            id: 0,
        });
    });
    if (!lattice) {
        return ase;
    }
    const { a, b, c, alpha, beta, gamma, matrix, spacegroup } = lattice;
    ase.angle = [alpha, beta, gamma];
    ase.length = [a, b, c];
    ase.spacegroup = [spacegroup.no, spacegroup.symbol];
    ase.matrix = matrix;

    return ase;
}
