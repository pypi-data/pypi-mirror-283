import { createContext, useCallback, useContext } from 'react';
import { ReactContextError, SimpleProvider } from '@@shared/utils/react';
import { useAppContext } from '@context';
import { getTokenFromCookie } from '@@@/lib/sso';
import { getExtByName, getNameByPath } from '@@shared/model/workspace/node/util';
import { exportASE2CloudDiskReq, exportASE2FileReq, getASEByCloudDiskReq, getASEByFileReq } from '@@api';
import { useMaterial3DCore } from './core';
import { MaterialCore } from '../core';
import { MaterialFormat } from '../model';
import { downloadFileFromBlob } from '@@shared/utils/util';

async function readFileText(file: File): Promise<string> {
    return new Promise(resolve => {
        const reader = new FileReader();
        reader.onload = (ev: ProgressEvent<FileReader>) => {
            const result = ev?.target?.result || '';
            resolve(result as string);
        };
        reader.readAsText(file);
    });
}

const EmptyAseData = {
    atoms: [],
};

const useContextValue = () => {
    const { coreRef, render } = useMaterial3DCore();
    const { userInfo } = useAppContext();

    const readData = useCallback(async (fileContent: string, format: MaterialFormat) => {
        const res = await getASEByFileReq({
            fileContent,
            format,
        });

        const core = new MaterialCore();
        core.setByASE(res?.data[0] || EmptyAseData);
        render(core, {
            changeFile: false,
        });
    }, []);

    const readFile = useCallback(async (file: File) => {
        const fileContent = await readFileText(file);
        const ext = getExtByName(file.name);
        await readData(fileContent, ext as MaterialFormat);
    }, []);

    const readCloudDisk = useCallback(async (params: { projectId?: number; userId?: number; path: string }) => {
        const name = getNameByPath(params.path);
        const ext = getExtByName(name);
        let origin = window.location.origin;
        if (origin.includes('localhost')) {
            origin = `https://bohrium.test.dp.tech`;
        }
        const searchParams = new URLSearchParams();
        searchParams.set('projectId', String(params.projectId || 0));
        searchParams.set('userId', String(params.userId || userInfo?.userId));
        searchParams.set('token', getTokenFromCookie()!);
        const fileUrl = `${origin}/bohrapi/v1/file/download/${params.path}?${searchParams.toString()}`;
        const res = await getASEByCloudDiskReq({
            fileUrl,
            format: ext,
        });
        const core = new MaterialCore();
        core.setByASE(res?.data[0] || EmptyAseData);
        render(core, {
            changeFile: false,
        });
    }, []);

    const download = useCallback(async (name: string) => {
        const ase = coreRef.current?.getAse();
        const format = getExtByName(name);
        if (!ase) {
            return;
        }
        const res = await exportASE2FileReq({
            fileContent: [ase],
            format,
        });

        downloadFileFromBlob(res.data, 'text/plain', name);
    }, []);

    const saveToCloudDisk = useCallback(async (params: { projectId?: number; path: string }) => {
        const { projectId, path } = params;
        const ase = coreRef.current?.getAse();
        const name = path.slice(path.lastIndexOf('/') + 1);
        const format = getExtByName(name);
        if (!ase) {
            return;
        }
        return exportASE2CloudDiskReq({
            fileContent: [ase],
            projectId: projectId || 0,
            path,
            format,
        });
    }, []);

    return {
        readFile,
        readCloudDisk,
        readData,
        download,
        saveToCloudDisk,
    };
};

const Context = createContext<ContextValue | undefined>(undefined);

type ContextValue = ReturnType<typeof useContextValue>;

export const Material3DIOProvider: SimpleProvider = ({ children }) => {
    const value = useContextValue();

    return <Context.Provider value={value}>{children}</Context.Provider>;
};

export const useMaterial3DIO = () => {
    const context = useContext(Context);
    if (context == null) {
        throw new ReactContextError('Material3DIOProvider');
    }
    return context;
};
