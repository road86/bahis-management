import type {Action, Reducer, ThunkAction} from "@reduxjs/toolkit"
import {combineSlices, configureStore} from "@reduxjs/toolkit"
import {setupListeners} from "@reduxjs/toolkit/query"
import {permissionApiSlice} from "../features/permissions/permissionApiSlice.ts";
import {formApiSlice} from "../features/forms/formApiSlice.ts";
import {formSlice} from "../features/forms/formSlice.ts";
import {permissionSlice} from "../features/permissions/permissionSlice.ts";
import {userSlice} from "../features/users/userSlice.ts";
import {userApiSlice} from "../features/users/userApiSlice.ts";


// `combineSlices` automatically combines the reducers using
// their `reducerPath`s, therefore we no longer need to call `combineReducers`.
const rootReducer: Reducer = combineSlices(permissionApiSlice, formSlice, formApiSlice, permissionSlice, userApiSlice, userSlice);
// Infer the `RootState` type from the root reducers
export type RootState = ReturnType<typeof rootReducer>

// The store setup is wrapped in `makeStore` to allow reuse
// when setting up tests that need the same store config
export const makeStore = (preloadedState?: Partial<RootState>) => {
    const store = configureStore({
        reducer: rootReducer,
        // Adding the api middleware enables caching, invalidation, polling,
        // and other useful features of `rtk-query`.
        middleware: getDefaultMiddleware => {
            return getDefaultMiddleware().concat(
                permissionApiSlice.middleware,
                formApiSlice.middleware,
                userApiSlice.middleware,
            )
        },
        preloadedState,
    })
    // configure listeners using the provided defaults
    // optional, but required for `refetchOnFocus`/`refetchOnReconnect` behaviors
    setupListeners(store.dispatch)
    return store
}

export const store = makeStore()

// Infer the type of `store`
export type AppStore = typeof store
// Infer the `AppDispatch` type from the store itself
export type AppDispatch = AppStore["dispatch"]
export type AppThunk<ThunkReturnType = void> = ThunkAction<
    ThunkReturnType,
    RootState,
    unknown,
    Action
>
