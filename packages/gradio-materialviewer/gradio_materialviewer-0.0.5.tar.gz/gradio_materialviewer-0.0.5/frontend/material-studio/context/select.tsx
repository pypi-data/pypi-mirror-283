import { createContext, useCallback, useContext, useEffect, useRef } from 'react';
import { ReactContextError, SimpleProvider } from '@@shared/utils/react';
import { useMaterial3DCore } from './core';
import { Atom } from '../model';
import { Subject, Subscription } from 'rxjs';

const useContextValue = () => {
    const { lightPluginRef, coreRef } = useMaterial3DCore();

    const subscriptionRef = useRef<Subscription>();
    const selectSubjectRef = useRef(new Subject<Array<Atom & { index: number }>>());
    const selectModeSubjectRef = useRef(new Subject<boolean>());

    const setSelectMode = useCallback((allow: boolean) => {
        lightPluginRef.current?.managers.events.setAllowSelect(allow);
        subscriptionRef.current?.unsubscribe?.();
        if (allow) {
            // @ts-ignore
            subscriptionRef.current = lightPluginRef.current?.managers.selection.event.changed.subscribe(() => {
                const items = lightPluginRef.current?.managers.selection.structure.getSelectionCellItems();
                const ids = items?.[0]?.elementIds || [];
                const atoms = coreRef.current?.symmetry?.atoms;
                if (!atoms) {
                    return;
                }
                const selected = atoms.filter((atom, idx) => ids.includes(idx));
                selectSubjectRef.current.next(selected.map((atom, idx) => ({ ...atom, index: ids[idx] })));
            });
        } else {
            lightPluginRef.current?.managers.selection.clear();
            selectSubjectRef.current.next([]);
        }
        selectModeSubjectRef.current.next(allow);
    }, []);

    return {
        setSelectMode,
        selectSubjectRef,
        selectModeSubjectRef,
    };
};

const Context = createContext<ContextValue | undefined>(undefined);

type ContextValue = ReturnType<typeof useContextValue>;

export const Material3DSelectProvider: SimpleProvider = ({ children }) => {
    const value = useContextValue();

    return <Context.Provider value={value}>{children}</Context.Provider>;
};

export const useMaterial3DSelect = () => {
    const context = useContext(Context);
    if (context == null) {
        throw new ReactContextError('Material3DSelectProvider');
    }
    return context;
};
