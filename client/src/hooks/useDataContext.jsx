import { useContext } from "react";
import { CalendarContext, TaskContext } from "../context/DataContext";

const createUseContextHook = (Context, contextName) => {
    return () => {
            const context = useContext(Context)
            if (!context) {
                throw new Error(`use${contextName} must be used within a ${contextName}Provider`)
            }
            return context
    }
}

export const useCalendarContext = createUseContextHook(CalendarContext, 'Calendar')
export const useTaskContext= createUseContextHook(TaskContext, 'Task')
// export const useEventContext = createUseContextHook(EventContext, 'Event')
// export const useSentInviteContext = createUseContextHook(Sent_InviteContext, 'SentInvite')
// export const useReceivedInviteContext = createUseContextHook(Received_InviteContext, 'RecievedInvite')
// export const useOwnedCollaborationContext = createUseContextHook(Owned_CollaborationContext, 'OwnedCollaboration')
// export const useGuestCollaborationContext = createUseContextHook(Guest_CollaborationContext, 'GuestCollaboration')
