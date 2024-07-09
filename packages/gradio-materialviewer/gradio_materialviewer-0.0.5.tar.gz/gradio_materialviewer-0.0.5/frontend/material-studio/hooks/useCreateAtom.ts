import { useCallback, useRef, useState } from 'react';
import { Vec3 } from 'dpmol';
import { Subscription } from 'rxjs';
import { useMaterial3DCore } from '../context/core';
import { createAtom, getElementLociInfo } from '../utils/utils';

export function useCreateAtom() {
    const { lightPluginRef, coreRef, render } = useMaterial3DCore();
    const subscriptionRef = useRef<Subscription>();
    const elementRef = useRef('C');

    const addAtom = useCallback((xyz: Vec3) => {
        if (!coreRef.current?.origin) {
            return;
        }
        const { origin } = coreRef.current;
        const atom = createAtom(
            {
                element: elementRef.current,
                xyz,
            },
            {
                order: origin.atoms.length,
            }
        );
        origin.atoms.push(atom);
        coreRef.current.setByOriginMaterial(origin);
        render(coreRef.current);
    }, []);

    const startCreateAtom = useCallback(() => {
        subscriptionRef.current?.unsubscribe();
        if (!lightPluginRef.current) {
            return;
        }
        lightPluginRef.current.canvas3d?.controls.setLockCameraState(true);
        // @ts-ignore
        subscriptionRef.current = lightPluginRef.current.canvas3d?.interaction.click.subscribe(ev => {
            if (!ev || !ev.page || !ev.current) {
                return;
            }
            const pos = lightPluginRef.current!.canvas3d?.getPosition(ev.page[0], ev.page[1]);
            if (!pos?.position) {
                return;
            }
            const { loci } = ev.current;
            if (loci.kind !== 'element-loci') {
                return addAtom(pos.position);
            }

            // TODO: position = selected.r + bond(selected => el)
            const info = getElementLociInfo(loci);
            if (!info) {
                return;
            }
            const offsetConstant = 0.5;
            const offset = {
                x: offsetConstant,
                y: offsetConstant,
                z: offsetConstant,
            };
            const position = Vec3.create(info.x + offset.x, info.y + offset.y, info.z + offset.z);
            addAtom(position);
        });
    }, []);

    const endCreateAtom = useCallback(() => {
        subscriptionRef.current?.unsubscribe();
        lightPluginRef.current?.canvas3d?.controls.setLockCameraState(false);
    }, []);

    const setElement = useCallback((el: string) => {
        elementRef.current = el
    }, []);

    return {
        elementRef,
        setElement,
        startCreateAtom,
        endCreateAtom,
    };
}
